import json
from pathlib import Path
from pprint import pprint

def run():
    print("This is your PRIVATE data you can manually use it to send your request if you want.")
    print("If they are empty, something went wrong (report on GitLab, DON'T SHARE YOUR contractId).")

    result = {
        "refillThresholdValueUid": None,
        "contractId": None,
        "resourceId": None,
        "billingAccountId": None,
        "offerId" : None
    }

    base_path = Path(__file__).parent
    user_data_dir = base_path / "user_data"
    user_data_dir.mkdir(exist_ok=True)

    offers_path = user_data_dir / "offers-data.json"
    nav_path = user_data_dir / "navigation-list.json"
    user_data_path = user_data_dir / "userdata.json"

    try:
        # Extract from offers-data.json
        if offers_path.exists():
            with open(offers_path, encoding="utf-8") as f:
                offers_data = json.load(f)
            first_offer = (offers_data.get("subscribedOffers") or [{}])[0]
            result.update({
                "refillThresholdValueUid": first_offer.get("refillThresholdValueUid"),
                "resourceId": first_offer.get("resourceId"),
                "contractId": first_offer.get("subscriptionId"),
                "offerId": first_offer.get("offerId")
            })

        # Extract from navigation-list.json
        if nav_path.exists():
            with open(nav_path, encoding="utf-8") as f:
                nav_data = json.load(f)

            subscriptions = (
                nav_data.get("userDetails", {})
                .get("subscriptions", [])
            )
            if subscriptions:
                first_sub = subscriptions[0]
                if not result["contractId"]:
                    result["contractId"] = first_sub.get("contractId")
                result["billingAccountId"] = first_sub.get("billingAccountId")

        # Write to output file
        with open(user_data_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        pprint(result)
        return True

    except json.JSONDecodeError as e:
        print(f"Invalid data in one of the files: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")

    return False

if __name__ == "__main__":
    run()
