# Telegram Bot
CZ1003 Project
bot-project

# Pre-requisites
## Installing Dependencies

### **1. Telepot module**
```
pip install telepot
```
	
### **2. Beautifulsoup module**
```
pip install beautifulsoup4
```

### **3. Splinter module**
```
pip install splinter
```

### **4. Google API module**
```
pip install --upgrade google-api-python-client
```

### **5. Google Chrome Driver**
```
brew install chromedriver
```


### **6. openpyxl Package**
```
pip install openpyxl
```

## Setting Up Google API
### **Turn on the Google API of your account**
Refer to the [Google's official documentation](https://developers.google.com/google-apps/calendar/quickstart/python).
> Important Notes: save the .json file in the *[resources/api/](resources/api)* folder under the name of *client_secret.json*.


# User Manual

Welcome to our bot! We will help you maneuver your WAY through your DAY!
Feel free to ask me stuff :)
If you want to know your course schedule, type in COURSE. If you want to plan your meetings, type in MEETINGS. If you want to know anything about me, just type in whatever you want and hope I understand :)

## Contents

### [Chapter 1 Introduction](#chapter-1-introduction-1)

#### 1.1 Overview

#### 1.2 System Requirements

### [Chapter 2 Getting Started](#chapter-2-getting-started-1)

#### 2.1 IDLE Python 3.6

#### 2.2 Visual Studio Code 1.15.1 Python 3.6

### [Chapter 3 Inputing Course Indexes and Finding Common Free Time](#chapter-3-inputing-course-indexes-and-finding-common-free-time-1)

#### 3.1 Inputting Your Index 
##### 3.1.1 Selecting Student Type
##### 3.1.2 Adding your First Week and First Recess Week

#### 3.2 Creating New Event

#### 3.3 Check If You Are Free at A Certain Time 




## Chapter 1 Introduction

### 1.1 Overview

This bot is a software written to help NTU students keep track of their course schedule. 
This bot also allows NTU students or NTU Bot Users to compare their respective schedules. 
Hence, you can find common free time to get together for various meetings. 

### 1.2 System Requirements

The bot requires Telegram versions released after 9 April, 2016 or Telegram Web.

## Chapter 2 Getting Started

We have several alternatives to run the program as to which Python platform you choose to use.

### 2.1 IDLE Python 3.6

To start the program, you should first open IDLE Python3.6.
Then open file “first_thing.py” found in the "samples" folder. 
Then click “Run” and choose “Run Module” to start the bot. 
You will be able to see the text “Listening ...” printed on the screen, indicating that your code is currently running.

### 2.2 Visual Studio Code 1.15.1 Python 3.6

To start the program, you should first open Visual Studio Code 1.15.1 Python 3.6. 
Then open file "first_thing.py" found in the "samples" folder. Then rightclick and choose "Run Code" if your default Programming language is Python 3.6 or "Run Python File in Terminal" if your default Programming language is not Python 3.6. You will be able to see the text "Listening ..." printed on the screen, indicating that your code is currently running.


## Chapter 3 Inputing Course Indexes and Finding Common Free Time

### 3.0 Starting The Bot

To start the bot, say "hi" to the bot and wait for it to greet you.
Then ask what the bot can do by asking "what do you do?", or you can simply type in "/start". 
You can then talk to the bot and ask it to arrange your meet

### 3.1 Inputting Your Index

You can input your index in the bot. This way, the bot can tell you what courses you have throughout the day. To input your course's index, you must first type in **/addindex**
If you have not completed some of your index, the bot will then redirect you to another instructions that you have to fullfill before adding your index.
The bot will reply in the following manner:
```
Sure thing.

Hmm... Wait a second. You haven't told me what enough data!

Run /setstudenttype or /st to set your student_type, i.e. Full Time or Part Time

Run /addfirstweek to set your first_week and first_recess_week
```
#### 3.1.1. Setting Student Type

You must set your student type before putting in your index. This is equivalent to declaring whether you are a part time student or a full time student.
To do this, you must first type in **/setstudenttype** or **/st**
The bot will then reply in the following manner:
```
Are you a full time or part time student?

```
You will be given two choices in the keyboard; "Full-Time Student" and "Part-Time Student". Click your Student Type. The bot will reply in the following manner:
```
Successful!
```
#### 3.1.2. Adding your First Week and First Recess Week

You must also enter your first week and first recess week in your bot. To do that, you must first enter **/addfirstweek** into the bot. 
```
Please Enter your first week and first recess week using the following format:

FirstWeek;FirstRecessWeek

For example:

2017-8-14;2017-10-2
```
Enter the dates in the above format. After you enter the dates, the bot will reply in the following manner:
```
Captured!

Your data is sucessfully recorded in our database!
```
After you have completed the process above, enter **/addindex** into the bot, and the bot should reply you in the following manner:
```
Sure thing. Please type your details in following format:

Please type your course code below. For example, CZ1003
```
Type in your course code and the bot will output a keyboard listing all the indexes in that course. 

### 3.2 Creating New Event

You can create new events through the bot and the bot will input it in your Google Calendar for you.
First, type in **/createevent** to create your event.
The bot will respond in the following manner:
```
Okay send me the details in following format:

Event Name;location;yyyy-mm-ddThh:mm:ss;yyyy-mm-ddThh:mm:ss
```
Input the details of your event according to the format above.
The bot will return **Successful!** if your event creation is successful.

**NOTE: the 'T' indicates a separation between the date and time of the event.
You must include the 'T' in your input.**

### 3.3 Check If You Are Free At A Certain Time

You can check whether you are free at a particular time through the bot.
First, type in **/isfree** to check if you are free at that particular time.
The bot will respond in the following manner:
```
Please enter the date interval using the following format:

YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM
```
Input the details in the format above.
If you are free at that particular time interval, the bot will respond in this following manner:
```
True

You are free on this time interval
```
However if you are not free at that particular time interval, the bot will respond in this following manner:

```
False

You are busy on this interval!

You have an event from 2017-09-21T21:00:00+08:00 to 2017-09-21T22:00:00+08:00
```

### 3.4 Choose Meeting Time According to Bot Recommendation

This bot also offers the function to predict how many people will be in the section you are going to. Accessing the interface where two buttons “Library Current Status Inquiry” and “Library Status Prediction” are presented, you are expected to click on the latter. After that, do the same as the above-mentioned step to focus on one section. The program will return you a computed number, which is the average of the last several sets of data collected.
