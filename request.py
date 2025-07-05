import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import sys


LOGIN_URL = 'https://www.alditalk-kundenportal.de'
SUCCESS_URL = 'https://www.alditalk-kundenportal.de/portal/auth/uebersicht/'

PAYLOAD_URL = 'https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/selfcare-dashboard/v1/offer/updateUnlimited'
USER_DATA_DIR = Path("./user_data")
USERDATA_JSON = USER_DATA_DIR / "userdata.json"

async def main(num_requests):
    if not USERDATA_JSON.exists():
        print(f"Missing {USERDATA_JSON}. Please create it with ./auto-refill get and then ./auto-refill extract first.")
        return

    with USERDATA_JSON.open("r", encoding="utf-8") as f:
        user_data = json.load(f)

    payload_data = {
        "amount": user_data.get("refillThresholdValueUid"),
        "offerId": user_data.get("offerId"),
        "refillThresholdValue": user_data.get("refillThresholdValueUid"),
        "subscriptionId": user_data.get("contractId"),
        "updateOfferResourceID": user_data.get("resourceId"),
    }

    if not all(payload_data.values()):
        print(" some fields are missing in userdata.json, try the above action again, and if doesnt work, please report it on gitlab")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(str(USER_DATA_DIR), headless=True)
        page = browser.pages[0] if browser.pages else await browser.new_page()

        if page.url.startswith(SUCCESS_URL):
            print("Already logged in.")
        else:
            print("Opening login page...")
            await page.goto(LOGIN_URL)
            print("Waiting for login...")
            await page.wait_for_url(SUCCESS_URL, timeout=10 * 60 * 1000)

        print(f"Login Successful. Sending {num_requests} request(s)...")

        for i in range(num_requests):
            try:
                response = await page.evaluate(
                    """async ({url, payload}) => {
                        const res = await fetch(url, {
                            method: 'POST',
                            credentials: 'include',
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                            },
                            body: JSON.stringify(payload)
                        });
                        return {status: res.status, body: await res.json()};
                    }""",
                    {"url": PAYLOAD_URL, "payload": payload_data}
                )
                print(f"Request {i + 1} (HTTP {response['status']})")
                print(json.dumps(response["body"], indent=2))
            except Exception as e:
                print(f"something went wrong, try again maybe")
                break

        await browser.close()

def run():
    NUM_REQUESTS = 1

    print(f"Requesting {NUM_REQUESTS} time(s)")
    asyncio.run(main(NUM_REQUESTS))
