# Telegram Bot
CZ1003 Project
bot-project

# Pre-requisites
## Installing Dependencies

### 1. Telepot module
```
pip install telepot
```
	
### 2. Beautifulsoup module
```
pip install beautifulsoup4
```

### 3. Splinter module
```
pip install splinter
```

### 4. Google API module
```
pip install --upgrade google-api-python-client
```

### 5. openpyxl Package
```
pip install openpyxl
```

### 6. pytz Package
```
pip install pytz
```

### 7. Browser Driver
Assuming you are using Google Chrome, then run the following command:
```
brew install chromedriver
```
If you are using Mozilla Firefox, then read the [Documentation for geckodriver](https://github.com/mozilla/geckodriver)



# User Manual

Hi! Need help to be more productive? Good news, I'm here to manage your time! Feel free to ask me stuff :)

Want to add course index? Just run /addindex.

Want to plan your meetings? Just type in 'meetings' and let me schedule it for you.

Want to know me more? Just ask me whatever you want and hope I can understand :)

To know more commands just type forward slash '/' to see what's available

## Contents

### [Chapter 1 Introduction](#chapter-1-introduction-1)

#### 1.1 Overview

#### 1.2 System Requirements


### [Chapter 2 Getting Started](#chapter-2-getting-started-1)

#### 2.1 Setting Up Telegram bot token

#### 2.2 Setting Up Google API

#### 2.3 Setting Up Browser

#### 2.4 Testing your Bot


### [Chapter 3 Inputing Course Indexes and Finding Common Free Time](#chapter-3-inputing-course-indexes-and-finding-common-free-time-1)

#### 3.1 Inputting Your Index 
##### 3.1.1 Selecting Student Type
##### 3.1.2 Adding Your First Week and First Recess Week
##### 3.1.3 Adding Your Course Code

#### 3.2 Creating New Event

#### 3.3 Check If You Are Free at A Certain Time

#### 3.4 Removing Your Index




## Chapter 1 Introduction

### 1.1 Overview

This bot is a software written to help NTU students keep track of their course schedule. 
This bot also allows NTU students or NTU Bot Users to compare their respective schedules. 
Hence, you can find common free time to get together for various meetings. 

### 1.2 System Requirements

1. Telegram versions released after 9 April, 2016 or Telegram Web.
2. Python 3.6x


## Chapter 2 Getting Started

Before you can run the bot, several settings are required. 

### 2.1 Setting Up Telegram Bot

1. To set up a bot, read the [Telegram's official documentation](https://core.telegram.org/api).
2. After you receive the token, save it in the **[resources/](resources/)** folder under the name of **token.txt**

### 2.2 Setting Up Google API

1. Turn on your Google API by following the [Google's official documentation](https://developers.google.com/google-apps/calendar/quickstart/python)
2. After you receive your API (.json file), save it in the **[resources/api/](resources/api)** folder under the name of **client_secret.json**.

### 2.3 Setting Up Browser

Write your browser name (i.e. *chrome* or *firefox*) and save it in the **[resources/](resources/)** folder under the name of **browser.txt**

>**Important Notes**: Your browser must have its driver in order to work. [Refer to step in the pre-requisite section](#7-browser-driver)

### 2.4 Testing your Bot

1. Run your Bot

To start the program, run file **app.py** in the **[main/](main/)** folder. 
You will be able to see the text *Listening ...* printed on the console, indicating that your code is currently running.

2. Say *"Hi"* to your Bot

Try sending the message *"Hi"* to your bot. If it replies *"Hi, <your_name>!"*, then you're all set!


## Chapter 3 Inputing Course Indexes and Finding Common Free Time


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

#### 3.1.3 Adding Your Course Code

After you have completed the process above, enter **/addindex** into the bot, and the bot should reply you in the following manner:
```
Sure thing. Please type your details in following format:

Please type your course code below. For example, CZ1003
```
Type in your course code and the bot will output a keyboard listing all the indexes in that course as a mark-up keyboard and will return to you thr following message:
```
The indexes for this course code has been successfully accessed. Please do the instructions above :)
```
Click on your course index **once** and if addition of course schedule is successful, your bot will reply in the following manner:
```
Nice!
00317 has been added to your Google Calendar
```
where **00317** is the index of your course.

### 3.2 Creating New Event

You can create new events through the bot and the bot will input it in your Google Calendar for you.
First, type in **/addevent** to create your event.
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

### 3.4 Removing Your Index

You can remove your index if you have put in the wrong index, or if you have simply dropped the course.To remove your index, simply type in **/removeindex** into the bot. The bot will respond in the following manner:

```
Please type the course code that you want to remove!
```
After the bot replied as above, type in the course code you want to remove, i.e. CZ1003.
After you have typed in the course code that you want to remove, the bot will reply as follows if the removal is a success:
```
Removing index...

The index for this course code has been removed from your Google Calendar and our database!

Run /addindex to replace your removed index, if you wish :D
```
If removal is not successful, it may be caused by you entering the wrong course code and the bot will reply in the following manner:
```
Removing index...

Cannot remove index!
```
