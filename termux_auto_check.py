import json
import requests
import time
import subprocess
from pathlib import Path

USER_DATA_DIR = Path("./user_data")
USERDATA_JSON = USER_DATA_DIR / "userdata.json"

USED_AMOUNT13GB = 3_145_728
USED_AMOUNT5GB = 10_485_760
USED_AMOUNT2GB = 13_631_488 
USED_AMOUNT1GB = 14_284_024
USED_AMOUNT9MB = 14_680_640  



INTERVAL_SECONDS = 80     # Time between checks

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


def load_cookies():
    cookies_file = USER_DATA_DIR / "cookies.json"
    try:
        with open(cookies_file, encoding="utf-8") as f:
            raw_cookies = json.load(f)
        session_cookies = {cookie["name"]: cookie["value"] for cookie in raw_cookies}
        return session_cookies
    except Exception as e:
        print(f"❌ Failed to load cookies: {e}")
        return {}


def fetch_offers(contract_id, billing_id, max_retries=3):
    billing_trimmed = billing_id[2:] if len(billing_id) > 2 else billing_id
    offers_url = (
        f"https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/"
        f"selfcare-dashboard/v1/offers/C-{billing_trimmed}"
        f"?warningDays=1&contractId={contract_id}"
    )

    cookies = load_cookies()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
        "Accept": "application/json",
        "Referer": "https://www.alditalk-kundenportal.de/portal/auth/uebersicht/",
    }

    for attempt in range(1, max_retries + 1):
        print(f"🌐 Attempt {attempt}/{max_retries} to fetch offers...")
        try:
            response = requests.get(offers_url, headers=headers, cookies=cookies, timeout=20)
            if response.status_code == 200:
                print("✅ Offer data fetched.")
                return response.json()
            else:
                print(f"❌ Server returned status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print("🔁 Retrying in 5 seconds...\n")
                time.sleep(5)
            else:
                print("❌ All fetch attempts failed.")
                return None

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
            if used >= USED_AMOUNT9MB:
                print("✅ 'used' is above or equal to 1GB. Running command...")
                try:
                    subprocess.run(COMMAND_ON_LOW_USAGE, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ Command failed with error: {e}")
                TIMER = INTERVAL_SECONDS
            elif used >= USED_AMOUNT1GB:
                TIMER = INTERVAL_SECONDS * 1.5
                print(f"⏱ Setting timer to {TIMER} seconds (1GB+)")
            elif used >= USED_AMOUNT2GB:
                TIMER = INTERVAL_SECONDS * 2
                print(f"⏱ Setting timer to {TIMER} seconds (2GB+)")
            elif used >= USED_AMOUNT5GB:
                TIMER = INTERVAL_SECONDS * 8
                print(f"⏱ Setting timer to {TIMER} seconds (5GB+)")
            elif used >= USED_AMOUNT13GB:
                TIMER = INTERVAL_SECONDS * 16
                print(f"⏱ Setting timer to {TIMER} seconds (13GB+)")
            else:
                print("⏸ 'used' is below 1GB threshold.")

        print(f"⏳ Waiting {TIMER} seconds before next check...\n")
        time.sleep(TIMER)


if __name__ == "__main__":
    run_loop()
