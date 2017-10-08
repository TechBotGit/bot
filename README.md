<<<<<<< HEAD
<<<<<<< HEAD
# bot
=======
# Telegram Bot
>>>>>>> a4af7bb133925e07c6db7a2f4164eb4bffa23c8e
=======
# Telegram Bot
>>>>>>> fae46f24934c73c34f9b0f2a5ef22553b5145270
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

<<<<<<< HEAD
### **5. Google Chrome Driver**
```
brew install chromedriver
```


### **6. openpyxl Package**
```
pip install openpyxl
```

=======
>>>>>>> fae46f24934c73c34f9b0f2a5ef22553b5145270
## Setting Up Google API
### **Turn on the Google API of your account**
Refer to the [Google's official documentation](https://developers.google.com/google-apps/calendar/quickstart/python).
> Important Notes: save the .json file in the *[resources/api/](resources/api)* folder under the name of *client_secret.json*.

<<<<<<< HEAD
<<<<<<< HEAD
Skip to content
This repository
Search
Pull requests
Issues
Marketplace
Explore
 @gabherondale
 Sign out
 Watch 0
  Star 0
  Fork 2 Archonsh/cz1003project
 Code  Issues 0  Pull requests 0  Projects 0  Wiki Insights 
Branch: master Find file Copy pathcz1003project/README.md
982d7fd  on 30 Sep 2016
@Archonsh Archonsh Update README.md
1 contributor
RawBlameHistory     
106 lines (72 sloc)  3.7 KB
CZ 1003 Project

User Manual

User manual of SchedulerBot
=======

# User Manual
>>>>>>> a4af7bb133925e07c6db7a2f4164eb4bffa23c8e
=======

# User Manual
>>>>>>> fae46f24934c73c34f9b0f2a5ef22553b5145270

Welcome to our bot! We will help you maneuver your WAY through your DAY!
Feel free to ask me stuff :)
If you want to know your course schedule, type in COURSE. If you want to plan your meetings, type in MEETINGS. If you want to know anything about me, just type in whatever you want and hope I understand :)

<<<<<<< HEAD
<<<<<<< HEAD
Contents
=======
## Contents
>>>>>>> fae46f24934c73c34f9b0f2a5ef22553b5145270

### [Chapter 1 Introduction](#chapter-1-introduction-1)

#### 1.1 Overview

#### 1.2 System Requirements

### [Chapter 2 Getting Started](#chapter-2-getting-started-1)

#### 2.1 IDLE Python 3.6

<<<<<<< HEAD
#### 2.2 Visual Studio Code 1.15.1 Python 3.6
=======
#### 2.5 Updating the List of Commands of Your Bot
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521

### Chapter 3 List of Commands Available
#### 3.01 /start and /

<<<<<<< HEAD
#### 3.1 Inputting Your Index 
=======
#### 3.02 /addevent
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521

#### 3.03 /removeevent

<<<<<<< HEAD
#### 3.3 Check If You Are Free at A Certain Time 
=======
#### 3.04 /getevent

#### 3.05 /setstudenttype

#### 3.06 /addfirstweek

#### 3.07 /addcourse

#### 3.08 /removecourse

#### 3.09 /getcourse

#### 3.10 /isfree

#### 3.11 /quit

### [Chapter 4 Inputing Course Indexes and Finding Common Free Time](#chapter-3-inputing-course-indexes-and-finding-common-free-time-1)

### 4.1 Inputting Your Course

#### 4.1.1. Setting Student Type
#### 4.1.2. Adding your First Week and First Recess Week

#### 4.1.3 Adding Your Course Code

### 4.2 Removing Your Course

### 4.3 Displaying Your Courses

### 4.4 Creating New Event

### 4.5 Removing Your Event

### 4.6 Displaying Your Events

### 4.7 Check If You Are Free At A Certain Time
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521

#### 3.4 Choose Meeting Time According to Bot Recommendation



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
The bot will reply in the following manner:
```
Sure thing. Please type your details in following format:

Course Name;Course Type(Full/Part Time);Index Number
```

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
<<<<<<< HEAD
© 2017 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About
=======
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

#### 2.5 Updating the List of Commands of Your Bot
To be able to use the **/** command in your bot, you must first in put the Command List into BotFather.
To do that, you must first type in **/setcommands** into BotFather. 
BotFather will then ask you to choose **which bot** you want to set these commands for. Choose your Personal Assistant Bot.
Then copy the following and send it to BotFather:
```
start - This command is used to initially start the bot
addevent - This command is used to add your own personal events, for instance meetings or parties, etc. 
removeevent - This command is used to remove the personal events that you have added into the calendar. 
getevent - This command is used to display all the events you have put in your calendar.
setstudenttype - This command lets you tell the bot whether you are a Part Time Student or a Full Time Student.
addfirstweek - This command lets you enter the date of your first week and the date of your first recess week into the bot.
addcourse - This command allows you to add your courses according to your index into Google Calendar.
removecourse - This command allows you to remove the course schedule you have put into the Google Calendar.
getcourse - This command lets you display all the courses you have put in the Google Calendar.
isfree - This command lets you check whether you are free at a certain time interval or not. 
quit - This quits the bot.
```
After you have done this, everytime you type in **/**, the bot will suggest commands you might want to use. 

### Chapter 3 List of Commands Available

#### 3.01 /start
This command is used to initially start the bot. Type **/start** in the telegram bot chat and the bot will greet you and tell you what it can do. 

#### 3.02 /addevent
This command is used to add your own personal events, for instance meetings or parties, etc. 

#### 3.03 /removeevent
This command is used to remove the personal events that you have added into the calendar.

#### 3.04 /getevent
This command is used to display all the events you have put in your calendar.

#### 3.05 /setstudenttype
This command lets you tell the bot whether you are a Part Time Student or a Full Time Student. This is necessary as it will determine your schedule.

#### 3.06 /addfirstweek
This command lets you enter the date of your first week and the date of your first recess week into the bot. This lets the bot determine your first week, thus letting it know your second week, third week, and so on. 
This will be used when you add your index as some of your LAB and LECTURE schedule happens on odd or even or random weeks. Thus you do not need to manually input your LAB and LECTURE schedule manually as your bot will automatically do it for you. With this command, you no longer have to manually remember the number of the week it is today or whether today is an odd week or an even week. 

#### 3.07 /addcourse
This command allows you to add your courses according to your index into Google Calendar. Hence your weekly school schedule will always be displayed in your Google Calendar. You do not have to worry about the odd and even week distribution of the LAB sessions and LECTURE as your bot has automatically input your schedule for you based on your first week and first recess week that you have set above.

#### 3.08 /removecourse
This command allows you to remove the course schedule you have put into the Google Calendar.

<<<<<<< HEAD
### 3.0 Starting The Bot

To start the bot, say "hi" to the bot and wait for it to greet you.
Then ask what the bot can do by asking "what do you do?", or you can simply type in "/start". 
You can then talk to the bot and ask it to arrange your meet
=======
#### 3.09 /getcourse
This command lets you display all the courses you have put in the Google Calendar.
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521

#### 3.10 /isfree
This command lets you check whether you are free at a certain time interval or not. 

#### 3.11 /quit
This quits the bot.

## Chapter 4 Inputing Course Indexes and Finding Common Free Time


### 4.1 Inputting Your Course

You can input your course in the bot. This way, the bot can tell you what courses you have throughout the day. To input your course's index, you must first type in **/addcourse**
If you have not completed some of your index, the bot will then redirect you to another instructions that you have to fullfill before adding your index.
The bot will reply in the following manner:
```
Sure thing.

Hmm... Wait a second. You haven't told me what enough data!

Run /setstudenttype or /st to set your student_type, i.e. Full Time or Part Time

Run /addfirstweek to set your first_week and first_recess_week
```
<<<<<<< HEAD
#### 3.1.1. Setting Student Type
=======

#### 4.1.1. Setting Student Type
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521

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
<<<<<<< HEAD
#### 3.1.2. Adding your First Week and First Recess Week
=======

#### 4.1.2. Adding your First Week and First Recess Week
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521

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
<<<<<<< HEAD
After you have completed the process above, enter **/addindex** into the bot, and the bot should reply you in the following manner:
=======

#### 4.1.3 Adding Your Course Code

After you have completed the process above, enter **/addcourse** into the bot, and the bot should reply you in the following manner:
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521
```
Sure thing. Please type your details in following format:

Please type your course code below. For example, CZ1003
```
Type in your course code and the bot will output a keyboard listing all the indexes in that course. 

### 4.2 Removing Your Course

You can remove your index if you have put in the wrong index, or if you have simply dropped the course.To remove your index, simply type in **/removecourse** into the bot. The bot will respond in the following manner:

```
Please type the course code that you want to remove!
```
After the bot replied as above, type in the course code you want to remove, i.e. CZ1003.
After you have typed in the course code that you want to remove, the bot will reply as follows if the removal is a success:
```
The course with this index has been removed from your Google Calendar and our database!

What you probably want to do next:

Run /addcourse to replace your removed course, if you wish

Run /removecourse to remove another course

Run /getcourse to list all the courses you have added
```
If removal is not successful, it may be caused by you entering the wrong course code and the bot will reply in the following manner:
```
Removing index...

Cannot remove index!
```
If you have no courses to remove, the bot will return you this following message:
```
There is nothing to remove...

What you probably want to do next:

Run /addcourse to add a course
```
### 4.3 Displaying Your Courses

To display the Courses you have put into your Google Calendar, simply type in **/getcourse**. The bot will respond by listing your courses and displaying it in a markup keyboard style.
It will also suggest other commands related to **/getcourse** that you might want to try out.
```
What you probably want to do next:

Run /addcourse to add a course

Run /removecourse to remove a course (if any)
```
If you have no courses added into your Google Calendar, your bot will return you the following message:
```
There is no course recorded in our database!

Run /addcourse to add your event!
```
### 4.4 Creating New Event

You can create new events through the bot and the bot will input it in your Google Calendar for you.
First, type in **/addevent** to create your event.
The bot will respond in the following manner:
```
Okay send me the details in following format:

Event Name;location;YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM

For example: Party;NTU;2017-10-08 20:00;2017-10-08 22:00
```
Input the details of your event according to the format above.
The bot will return **Successful!** if your event creation is successful.

### 4.5 Removing Your Event

You can remove the events you have put in your Google Calendar by typing in **/removeevent** to your bot. 
The bot will display the events you currently have on your calendar as a markup keyboard. Click on the event you want to remove and wait for the success message as shown below:
```
The event Party;2017-10-08 17:00;2017-10-08 18:00 has been removed!

What you probably want to do next:

Run /removeevent to remove another event!

Run /addevent to add an event!
```

If you have no event in your Google Calendar, the bot will return you this following message:
```
There is nothing to remove...

What you probably want to do next:

Run /addevent to add an event
```
### 4.6 Displaying Your Events

To display your events, you must first type in **/getevent** into the bot. The bot will then display the events you have in your Google Calendar in a markup keyboard style. It will also suggest you other commands you might want to try out as shown below:

```
What you probably want do next:

Run /removeevent to remove an event

Run /addevent to add an event
```
If there are no events in your Google Calendar, the bot will return you this following message:
```
There is no event recorded in our database!

Run /addevent to add your event!
```

### 4.7 Check If You Are Free At A Certain Time

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
<<<<<<< HEAD

### 3.4 Choose Meeting Time According to Bot Recommendation

This bot also offers the function to predict how many people will be in the section you are going to. Accessing the interface where two buttons “Library Current Status Inquiry” and “Library Status Prediction” are presented, you are expected to click on the latter. After that, do the same as the above-mentioned step to focus on one section. The program will return you a computed number, which is the average of the last several sets of data collected.
>>>>>>> a4af7bb133925e07c6db7a2f4164eb4bffa23c8e
=======
>>>>>>> fae46f24934c73c34f9b0f2a5ef22553b5145270
=======
>>>>>>> 38d0fb90211b31e2d73919c361fed6c0b3f61521
