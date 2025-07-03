import json
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

USER_DATA_DIR = Path("./user_data")
USERDATA_JSON = USER_DATA_DIR / "userdata.json"

USED_AMOUNT13GB = 3_145_728
USED_AMOUNT5GB = 10_485_760
USED_AMOUNT2GB = 13_631_488 
USED_AMOUNT1GB = 14_680_640  

INTERVAL_SECONDS = 120     # Time between checks
ADDED_TIME_SECONDS = 60   # This time will be added when you have too much, to save performance

COMMAND_ON_LOW_USAGE = ["python3", "refill.py", "request"]  # Command to execute

def load_user_data():
    try:
        with open(USERDATA_JSON, encoding="utf-8") as f:
            data = json.load(f)
            contract_id = data.get("contractId")
            billing_id = data.get("billingAccountId")
            if not contract_id or not billing_id:
                raise ValueError("Missing contractId or billingAccountId")
            return contract_id, billing_id
    except Exception as e:
        print(f"❌ Failed to load userdata: {e}")
        return None, None

def extract_used_value(offers):
    try:
        if isinstance(offers, str):
            offers = json.loads(offers)

        offers_list = offers.get("subscribedOffers", [])
        for offer in offers_list:
            pack = offer.get("pack", [])
            for item in pack:
                if item.get("type") == "data":
                    used_str = item.get("used")
                    if used_str is not None:
                        return int(used_str)
        print("⚠️ No 'used' value found for type 'data'.")
        return None
    except Exception as e:
        print(f"❌ Failed to parse 'used' value: {e}")
        return None

def fetch_offers(contract_id, billing_id):
    billing_trimmed = billing_id[2:] if len(billing_id) > 2 else billing_id
    offers_url = (
        f"https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/"
        f"selfcare-dashboard/v1/offers/C-{billing_trimmed}"
        f"?warningDays=1&contractId={contract_id}"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR.resolve()),
            headless=True,
        )
        page = browser.new_page()
        try:
            print("🔐 Visiting dashboard to initialize session...")
            page.goto("https://www.alditalk-kundenportal.de/portal/auth/uebersicht/", timeout=60_000)
            page.wait_for_load_state("networkidle")

            print(f"🌐 Fetching: {offers_url}")
            response = page.evaluate(f"""
                () => fetch("{offers_url}")
                    .then(res => res.json())
                    .catch(err => ({{error: err.toString()}}))
            """)
#    response is already a dict
#            If there is an Error unmark these and check the output
#            offers_file = USER_DATA_DIR / "offers-debug.json"
#            offers_file.write_text(json.dumps(response, indent=2), encoding="utf-8")
#
            return response
        finally:
            browser.close()

def run_loop():
    while True:
        print("🔁 Starting cycle...")
        contract_id, billing_id = load_user_data()
        if not contract_id or not billing_id:
            print("❌ Skipping due to missing user data.")
            time.sleep(INTERVAL_SECONDS)
            continue

        offers_json = fetch_offers(contract_id, billing_id)
        used = extract_used_value(offers_json)

        # Default fallback
        TIMER = INTERVAL_SECONDS  

        if used is None:
            print("⚠️ No 'used' value found.")
        else:
            print(f"📊 Current 'used' value: {used}")
            if used >= USED_AMOUNT1GB:
                print("✅ 'used' is above or equal to 1GB. Running command...")
                try:
                    subprocess.run(COMMAND_ON_LOW_USAGE, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ Command failed with error: {e}")
                TIMER = INTERVAL_SECONDS  # Fast check after refill
            elif used >= USED_AMOUNT2GB:
                TIMER = ADDED_TIME_SECONDS + INTERVAL_SECONDS
                print(f"⏱ Setting timer to {TIMER} seconds (2GB+)")
            elif used >= USED_AMOUNT5GB:
                TIMER = ADDED_TIME_SECONDS * 3 + INTERVAL_SECONDS
                print(f"⏱ Setting timer to {TIMER} seconds (5GB+)")
            elif used >= USED_AMOUNT13GB:
                TIMER = ADDED_TIME_SECONDS * 6 + INTERVAL_SECONDS
                print(f"⏱ Setting timer to {TIMER} seconds (13GB+)")
            else:
                print("⏸ 'used' is below 1GB threshold.")

        print(f"⏳ Waiting {TIMER} seconds before next check...\n")
        time.sleep(TIMER)


if __name__ == "__main__":
    run_loop()
