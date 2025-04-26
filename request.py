import requests

# Create a session
session = requests.Session()


#################################
# Manually set the cookies (Read the Readme on how to do it) 
cookies = {
    'AWSALB': 'your_aws_alb_cookie',
    'AWSALBCORS': 'your_aws_albcors_cookie',
    'rememberMe': 'true',
    'session_id': 'your_session_id',
    'user_id': 'your_user_id',
    'is_logged': 'true',
    # Add any other cookies you copied here
}
###################################


session.cookies.update(cookies)

# Headers (These are here to blend in)
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.alditalk-kundenportal.de',
    'Referer': 'https://www.alditalk-kundenportal.de/portal/auth/uebersicht/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}



# The URL for sending the payload 
payload_url = 'https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/selfcare-dashboard/v1/offer/updateUnlimited'




#########################################
# Manually set the payload (you will have to inspect the data in the network tab of your browser, Don't forget to enable the Presist Logs in your developer tab)
payload_data = {
    "amount": "",  # replace with your actual amount
    "subscriptionId": "",  # replace with your subscription ID
    "updateOfferResourceID": "",  # replace with the correct ID
}
########################################


# Limit for how many times the payload can be sent, if you go above aldi my detect this unusal behavior
MAX_TIMES = 5

# Ask for number of times, with validation for the limit
while True:
    num_times = int(input(f"How many request do you want to make (max {MAX_TIMES}): "))
    if 1 <= num_times <= MAX_TIMES:
        break
    print(f"Please enter a number between 1 and {MAX_TIMES}.")
    
    
    
    
# sending it
for _ in range(num_times):

    # Send the POST request with the payload
    response = session.post(payload_url, headers=headers, json=payload_data)

# Check if the request was successful
    if response.ok:
        print("Payload sent successfully!")
        print(response.text)
    else:
        print(f"Failed to send payload! Status: {response.status_code}")
        print(response.text) 
