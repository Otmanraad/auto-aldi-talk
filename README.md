# What is this Project

Well I got annoyed that I have to open the App and refill 1GB every single time, so I made this to automate the processes.


## Getting Started

this opens a chrome site where you have to log in into your account, 
once logged in the script will fetch some data from aldi-talk
and Save them in userdata
```
python refill.py get
```

this will extract contractId, ResouceID, etc from the data pulled from refill get
```
python refill.py extract
```

This will request one gigabyte if the threshold is lower then 1 GB and will refill the amount you can refill
```
python refill.py request.
```
This Will automaticly Check the threshold and if its lower then it will add
There is a Timer it will check the threshold every 120 sec (it take 160 sec to use 1GB at 50MP,)
if the threshold is lower then it will auto refill you will never have to check the ALdi talk anymore atleast for me
You will need to run this script for long time on a server or computer tho,

```
python auto_check
```


## Install Requirements

on Arch(if you are on diffrent system then try to find the packages and install them)
```
sudo pacman -S python python-pip git
```


## Installing Project

Clone the Project
```
git clone https://gitlab.com/raad.h.othman/auto-aldi-talk
```

Create envimorment
```
python3 -m venv aldi-talk-venv
```

Activate the envimorment
source Path/to/envimorment/aldi-talk/bin/activate
```
source aldi-talk/bin/activate
```

install python requirements
```
pip install -r requirements.txt
```

Install Playwright browser
```
playwright install
```




If you want to auto run it and never think again you can use Oracle Cloud, free tier, is really good and I got it working
and I havn#t vistied the website in a long time, 
just to inform you they change it quit a bit last time i had something working and they changed their API and backend
so if they change again it will break again


Either way this was mostly AI so I wanna  Thanks ChatGPT, at this point I lost what I made and what ChatGPT made I just give it and 
it just give me the best code, Playwright was ChatGPT Idea, I used pywebview, and lets just say I cloudn't make it work sadly, then
I used ChatGPT and boof it fixed everything.....





Feel free to fork and contribute Suggestions, bug reports, are welcome.


This project was made with the help of Deepseek and ChatGPT, Hopefully you won't hate me for it.
I used Deepseek last time and as you may know its trash compered to ChatGPT at this point, 
To clarify I remade the project and added automation, but it kept breaking so I never published it



At this Point more then 80% are made by AI, mostly ChatGPT Plus, it got Really Good, 
This is update cause last time I didnt update the Gitlab repo cause Aldi-Talk Changed alot of stuff, and I had to remake stuff alot of times