# What is this Project

Well I got annoyed that I have to open the App and refill 1GB every single time, so I made this to automate the processes right now its fully manual but is good enough

## How to Use it right now

You need to first get your cookies/Payload first, so this can request mutilple times for you.

First lets get your Id for your account.

Go to https://www.alditalk-kundenportal.de/portal/auth/uebersicht/

Then Open your developer menu(F12)

Go to the Network tab **(And Enable Presist Logs)**

Then click the Refill button you should get an entery in **XHR** called **updateUnlimited**

Click on **updateUnlimited** and go to Request Tab, you should see your 
```
    "amount": "111",
    "subscriptionId": "222",
    "updateOfferResourceID": "333",
```
Copy them and paste them in the **request.py** (around line 34-36)


now we need to get your cookies for your browser session,
Go to https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/selfcare-dashboard/v1/offer/updateUnlimited

and go to the Network Tab and click on updateUnlimited but this time you will get your Cookies at the bottom
Copy them and paste them in (Line 19),

then
```
cd auto-aldi-talk
# Don't forget to add your cookies and payload data.
python request.py
```
 you should be done now it should add the requested amount


## Project status
I'm kinda slow so is very likley that I won't update this for idk how long may even never update this too so you can do what ever you want with it.



## License
GNU AFFERO GENERAL PUBLIC LICENSE 
