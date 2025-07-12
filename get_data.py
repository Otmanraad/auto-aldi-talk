import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

LOGIN_URL = "https://www.alditalk-kundenportal.de"
SUCCESS_URL = "https://www.alditalk-kundenportal.de/portal/auth/uebersicht/"
NAVIGATION_URL = "https://www.alditalk-kundenportal.de/scs/bff/scs-207-customer-master-data-bff/customer-master-data/v1/navigation-list"

USER_DATA_DIR = Path("./user_data")
OUTPUT_NAVIGATION = USER_DATA_DIR / "navigation-list.json"
OUTPUT_OFFERS = USER_DATA_DIR / "offers-data.json"

USER_DATA_DIR.mkdir(exist_ok=True)

def find_value(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            result = find_value(v, key)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_value(item, key)
            if result:
                return result
    return None

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(str(USER_DATA_DIR), headless=False)
        page = browser.pages[0] if browser.pages else await browser.new_page()

        if not page.url.startswith(SUCCESS_URL):
            print("Opening login page...")
            await page.goto(LOGIN_URL)
            print("Please log in manually.")
            await page.wait_for_url(SUCCESS_URL, timeout=10 * 60 * 1000)

        print("Logged in. Fetching navigation-list...")

        nav_response = await page.evaluate(f"""
            async () => {{
                const res = await fetch("{NAVIGATION_URL}");
                return await res.text();
            }}
        """)
        OUTPUT_NAVIGATION.write_text(nav_response, encoding="utf-8")
        print(f"navigation-list saved to {OUTPUT_NAVIGATION}")

        try:
            nav_json = json.loads(nav_response)
            contract_id = find_value(nav_json, "contractId")
            billing_id = find_value(nav_json, "billingAccountId")

            if not contract_id or not billing_id:
                print("Could not find contractId or billingAccountId")
                return

            billing_id_trimmed = billing_id[2:] if len(billing_id) > 2 else billing_id
            print(f"Extracted contractId={contract_id}, billingAccountId={billing_id_trimmed}")

            offers_url = (
                f"https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/"
                f"selfcare-dashboard/v1/offers/C-{billing_id_trimmed}"
                f"?warningDays=1&contractId={contract_id}"
            )

            print(f"Fetching offers from: {offers_url}")
            offers_response = await page.evaluate(f"""
                async () => {{
                    const res = await fetch("{offers_url}");
                    return await res.text();
                }}
            """)

            OUTPUT_OFFERS.write_text(offers_response, encoding="utf-8")
            print(f"Offers data saved to {OUTPUT_OFFERS}")

            try:
                offers_json = json.loads(offers_response)
                print("Offers data parsed successfully")
            except json.JSONDecodeError:
                print("Offers data is not valid JSON")

        except Exception as e:
            print(f"Error processing data: {e}")

        #Save cookies to cookies.json for autocheck without playwright
        cookies = await browser.cookies()
        cookies_file = USER_DATA_DIR / "cookies.json"
        with open(cookies_file, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)
        print(f"Cookies saved to {cookies_file}")
        await browser.close()

def run():
    print("Obtaining User Credentials")
    asyncio.run(main())

