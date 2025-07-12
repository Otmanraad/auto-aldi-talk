# What is this Project

This Project aims to Automaticly Refill 1GB every time it goes below the threshold, Set by ALDI-TALK

I made it After I got annoyed that I have to open the App and refill 1GB every single time, 
so I automated the processes.

If you encounter any problem please feel free to open a issue.
## How to Use This project

this opens a chrome site where you have to log in into your account, 
once logged in the script will fetch User data from aldi-talk
and Save them in user_data/
```
python refill.py get
```

this will extract contractId, ResouceID, etc.. from the user data pulled from ```python refill get```
```
python refill.py extract
```

This will request 1GB once your userdata is available, if the threshold is higher then 1 GB it will do nothing.
```
python refill.py request.
```

This is the automatic processes, to use it you need computer that is running 24/7 you can get server for example oracle free Tier,
all you need is your user_data folder, transfer to the server and run it from there, 
it will check the amount you have and if you have less then 1GB then it will request automatically
```
python auto_check
```



## Install

on Arch(if you are on diffrent system then install **pip**, **python3**, **git**)
```
sudo pacman -S python python-pip git
```

Clone the Project
```
git clone https://gitlab.com/raad.h.othman/auto-aldi-talk
```

move into the folder
```
cd auto-aldi-talk
```

Create python envimorment
```
python3 -m venv aldi-talk-venv
```

Activate the envimorment using
```
source aldi-talk-venv/bin/activate
```

install python requirements
```
pip install -r requirements.txt
```

Install Playwright browser
```
playwright install
```


**Done**


## Contributers

Me, and ChatGPT. and orginaly it was Deepseek who helped me,(it didnt it only made thing worse for me) but after ChatGPT4-Plus came out, it was soo good that I ask it about pywebview 
to try salvage my code instead it just remade the whole project, and fixed every problem and used a whole diffrent setup with Playwright

I was using pywebview, and no matter what I did I couldn't get it to work the way I wanted,
but after Asking it it made me a whole new thing with Playwright, so spaical thanks to ChatGPT4, 50% was just ChatGPT4 so 
Thanks alot ChatGPT4.


## Info

If you want to auto run it and never think again you can use Oracle Cloud, free tier, is really good and I got it working, 
without any problem on the x86 AMD free model, you can also use other free models as well or use paid one, is your choice

just to inform you, they always change the backend ALID-TALK. so it may break again, so just wait for me to fix it, you can also open a issue

Feel free to fork and contribute Suggestions, bug reports, are welcome, Thanks alot for using my project Don't forget to star.
