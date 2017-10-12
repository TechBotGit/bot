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

### 7. lxml Package
```
pip install lxml
```

### 8. Browser Driver
Assuming you are using Google Chrome, then run the following command:
```
brew install chromedriver
```
If you are using Mozilla Firefox, then read the [Documentation for geckodriver](https://github.com/mozilla/geckodriver)



# User Manual

Hi! Need help to be more productive? Good news, I'm here to manage your time! Feel free to ask me stuff!

Want to know me more? Just ask me whatever you want and hope I can understand

Want to know what I can do? Just run /help to see commands that I can do to help you

## Contents

### [Chapter 1 Introduction](#chapter-1-introduction-1)

#### 1.1 Overview

#### 1.2 System Requirements

### [Chapter 2 Getting Started](#chapter-2-getting-started-1)


#### 2.1 Cloning repository to your local machine

#### 2.2 Setting Up Telegram bot token

#### 2.3 Setting Up Google API

#### 2.4 Setting Up Browser

#### 2.5 Testing your Bot

#### 2.6 Updating the List of Commands of Your Bot


### [Chapter 3 List of Commands Available](#chapter-3-list-of-commands-available-1)
#### 3.01 /start

#### 3.02 /addevent

#### 3.03 /removeevent

#### 3.04 /getevent

#### 3.05 /setstudenttype

#### 3.06 /addfirstweek

#### 3.07 /addcourse

#### 3.08 /removecourse

#### 3.09 /getcourse

#### 3.10 /isfree

#### 3.11 /getupcomingevent

#### 3.12 /help

#### 3.13 /quit


### [Chapter 4 Inputting Course Indexes and Finding Common Free Time](#chapter-4-inputting-course-indexes-and-finding-common-free-time-1)

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

### 4.8 See All Your Upcoming Events

### 4.9 To See All The Commands You Have In Your Bot

### [Chapter 5 Further Information](#chapter-5-further-information-1)




## Chapter 1 Introduction
> [Back to contents](#contents)

### 1.1 Overview

This bot is a software written to help NTU students keep track of their course schedule and personal events. 
This bot allows you to automatically access your course schedule from STARS. You no longer have to worry about **ODD** and **EVEN** weeks as well as lectures and seminars occuring on **random** weeks through out the semester as the bot will automatically handle it for you. 
The bot also reminds you to attend your lectures, tutorials, labs and events **one hour** before respective events start in form of a **push notification**.

To recapitulate, there is no need for you to print your class schedule from STARS planner anymore. Furthermore, you don't have to manually check your class schedule if you want to add any personal events of your own (this is highly prone to error!) as the bot will automatically tell you if you are free on that time interval or not. In short, you can say good bye to the mindblowing **ODD** and **EVEN** weeks!

### 1.2 System Requirements

1. Telegram versions released after 9 April, 2016 or Telegram Web.
2. Python3.6x

## Chapter 2 Getting Started
> [Back to contents](#contents)

We have several alternatives to run the program as to which Python platform you choose to use.

### 2.1 Cloning Repository to your local machine

**You need to clone this repository to your local machine.**
1. Navigate to any folder from your Terminal
2. Run `git clone https://github.com/TechBotGit/bot.git`
> To get the latest version of Git: Download it from the [Git's official documentation](https://git-scm.com/downloads)

### 2.2 Setting Up Telegram Bot

1. To set up a bot, read the [Telegram's official documentation](https://core.telegram.org/api).
2. After you receive the token, save it in the **[resources/](resources/)** folder under the name of **token.txt**

### 2.3 Setting Up Google API

1. Turn on your Google API by following the [Google's official documentation](https://developers.google.com/google-apps/calendar/quickstart/python)
2. After you receive your API (.json file), save it in the **[resources/api/](resources/api)** folder under the name of **client_secret.json**.

### 2.4 Setting Up Browser

Write your browser name (i.e. *chrome* or *firefox*) and save it in the **[resources/](resources/)** folder under the name of **browser.txt**

>**Important Notes**: Your browser must have its driver in order to work. [Refer to step in the pre-requisite section](#8-browser-driver)

### 2.5 Testing your Bot

1. Run your Bot

To start the program, run file **app.py** in the **[main/](main/)** folder. 
You will be able to see the text *Listening ...* printed on the console, indicating that your code is currently running.

2. Say *"Hi"* to your Bot

Try sending the message *"Hi"* to your bot. If it replies *"Hi, <your_name>!"*, then you're all set!

### 2.6 Updating the List of Commands of Your Bot
To be able to view the list of commands in your bot without the use of **/help** command, you must first in put the Command List into BotFather.

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
getupcomingevent - This command displays all your upcoming events 
help - this displays all the commands you can use in the bot
quit - This quits the bot.
```
After you have done this, everytime you type in **/**, the bot will suggest commands you might want to use. 


### Chapter 3 List of Commands Available
> [Back to contents](#contents)

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

#### 3.09 /getcourse
This command lets you display all the courses you have put in the Google Calendar.

#### 3.10 /isfree
This command lets you check whether you are free at a certain time interval or not. 

#### 3.11 /getupcomingevent
This command displays all your upcoming events

#### 3.12 /help
This command displays all the commands present in the bot

#### 3.13 /quit
This quits the bot.


## Chapter 4 Inputting Course Indexes and Finding Common Free Time
> [Back to contents](#contents)


### 4.1 Inputting Your Course

You can input your course in the bot. This way, the bot can tell you what courses you have throughout the day. To input your course's index, you must first type in **/addcourse**
If you have not completed some of your index, the bot will then redirect you to another instructions that you have to fullfill before adding your index.
The bot will reply in the following manner:
```
Sure thing

Hmm... Wait a second. You haven't told me enough data!

Run /setstudenttype to set your student type, i.e. Full Time or Part Time

Run /addfirstweek to set your first_week and first_recess_week
```

#### 4.1.1. Setting Student Type

You must set your student type before putting in your index. This is equivalent to declaring whether you are a part time student or a full time student.
To do this, you must first type in **/setstudenttype** or **/st**
The bot will then reply in the following manner:
```
Are you a full time or part time student?

```
You will be given two choices in the keyboard; "Full-Time Student" and "Part-Time Student". Click your Student Type. The bot will reply in the following manner:
```
Sucessfull! Your data has been recorded in our database!

Have you added your first week?

If you haven't, run /addfirstweek

If you have, then run /addcourse straight away!
```

#### 4.1.2. Adding your First Week and First Recess Week

You must also enter your first week and first recess week in your bot. To do that, you must first enter **/addfirstweek** into the bot. 
```
Please enter the Monday dates of your first week and first recess week using the following format:

FirstWeek;FirstRecessWeek

For example:

2017-8-14;2017-10-2

Notes: These two dates are very important. If you enter the wrong dates and add your course (i.e. by running /addcourse), consequently, your course schedule will be shifted by one or more weeks!
```
Enter the dates in the above format. After you enter the dates, the bot will reply in the following manner:
```
Sucessfull! Your data has been recorded in our database!

Have you set your student type?

If you haven't, run /setstudenttype

If you have, run /addcourse straight away!
```

#### 4.1.3 Adding Your Course Code

After you have completed the process above, enter **/addcourse** into the bot, and the bot should reply you in the following manner:
```
Sure thing. Please type your details in following format:

Please type your course code below. For example, CZ1003
```
Type in your course code and the bot will output the following message:
```
Please wait while we process your information. This may take around a minute.

To prevent crashing, please wait until the Success message has appeared.
```

Then the bot will display a keyboard listing all the indexes in that course along wit the message:
```
Please choose your index below.
 Click only one of them once!
```
and 
```
The indexes for this course code has been successfully accessed. Please do the instructions above :)
```
Pay careful attention to the second message. Click on the index **once**. This is very important, as clicking the twice may result in an error in your database.

After you have clicked on your chosen index, the bot will reply in this following manner:
```
Nice!

CZ1003 (index 10628) has been added to your Google Calendar and our database

What you probably want to do next:

Run /addcourse to add another course

Run /removecourse to remove a course

Run /getcourse to list all the courses you have added
```
The course schedule has now ben inputted in your Google Calendar.

### 4.2 Removing Your Course

You can remove your index if you have put in the wrong index, or if you have simply dropped the course.To remove your index, simply type in **/removecourse** into the bot. The bot will respond in the following manner:

```
Please click the course that you want to remove!
```
The bot will then display a keyboard listing all the courses you have inputted in your Google Calendar. Click on the course you want to remove **once**. 
Clicking the course you want to remove more than **once** may result in an error in your database.

If removal of course is successful, you will receive the following message from the bot:
```
Your data has been removed from our database and your Google Calendar!

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
There are no indexes registered in our database!

What you probably want to do next:

Run /addcourse to add your index
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
If addition of event is successful, the bot will return this following message:
```
Sucessfull! Your data has been recorded in our database!

What you probably want to do next:

Run /addevent to add another event

Run /removeevent to remove an event

Run /getevent to list all events you have added
```

If you are not free on that time span, you cannot create an event. For example you have an event on that time span you want to create a new event:
```
Party;NTU;2017-10-08 20:00;2017-10-08 22:00
```
Hence, the bot will return:
```
Cannot add event!

You have 1 event(s) occuring between 2017-10-08 20:00 and 2017-10-08 22:00

1. 2017-10-08 20:00 until 2017-10-08 22:00

What you probably want to do next:

Run /addevent to add another event with different datetime
```

### 4.5 Removing Your Event

You can remove the events you have put in your Google Calendar by typing in **/removeevent** to your bot. 
The bot will display the events you currently have on your calendar as a keyboard with the following format: **event_name;start_time;end_time**. Click on the event you want to remove and wait for the success message as shown below:
```
The event Party;2017-10-08 20:00;2017-10-08 22:00 has been removed!

Your data has been removed from our database and your Google Calendar!

What you probably want to do next:

Run /removeevent to remove another event

Run /addevent to add an event

Run /getevent to list all events you have added
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

What you probably want to do next:

Run /addevent to add an event
```

### 4.7 Check If You Are Free At A Certain Time

You can check whether you are free at a particular time through the bot.
First, type in **/isfree** to check if you are free at that particular time.
The bot will respond in the following manner:
```
Please enter the date interval using the following format:

YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM

For example:

2017-10-09 08:00;2017-10-09 16:00
```
Input the details in the format above.
If you are free at that particular time interval, the bot will respond in this following manner:
```
True

You are free on this time interval

What you probably want to do next:

Run /addevent to add an event for this interval time

Run /getevent to list all events you have added

Run /isfree again to check for another time
```
However if you are not free at that particular time interval, the bot will respond in this following manner:

```
False

You are busy on this time interval!

You have 3 event(s) occuring between 2017-10-09 08:00 and 2017-10-09 16:00

1. 2017-10-09 10:30 until 2017-10-09 12:30

2. 2017-10-09 13:30 until 2017-10-09 14:30

3. 2017-10-09 15:30 until 2017-10-09 16:00

What you probably want to do next:

Run /isfree again with different datetime
```
If there is something wrong with the date and time you have inputted, the bot will respond in this following manner:
```
Your format is correct, however we cannot perform the query to your Google Account

Chances are:

1. You have problems with your API keys

2. You entered a bad date, e.g. your end time is smaller than your start time

What you probably want to do next:

Resolve your API problem

Run /addevent again and give me a reasonable date interval
```

### 4.8 See All Your Upcoming Events

You can view your upcoming events through the **/getupcomingevents** command. The bot will respond in the following manner:

```
Please enter how many upcoming events are you looking for!

For example: 10
```
In the case where you entered **7**, the bot will reply in this following manner:
```
Getting 7 upcoming event(s) for you
Here they are!
```
And it will display the first seven of your upcoming events (including your courses).
It displays the **name of the event, date of the event and time interval of the event**.

### 4.9 To See All The Commands You Have In Your Bot

To see all the commands available in your bot, you may type in **/help** and the bot will display the commands available in the bot in the following manner:
```
Here is the list of commands that I can do:

Basic Commands 
/start - Send welcome message 
/help - list available commands 
/quit - Send good bye message 

General Commands 
/isfree - To check whether you are free at a certain time interval 
/getupcomingevent - List your upcoming events 

Event-related Commands 
/addevent - Add an event to your Google Calendar 
/removeevent - Remove an event from your Google Calendar 
/getevent - List all events that you have added 

Course-related Commands 
/addcourse - Add a course schedule to your Google Calendar 
/removecourse - Remove a course schedule from your Google Calendar 
/getcourse - List all courses that you have added 
/setstudenttype - Set your student type (Full Time or Part Time) 
/addfirstweek - Add the first weekday, i.e. Monday, of your first week and recess week
```

## Chapter 5 Further Information
> [Back to contents](#contents)
### Information 1: 

For any commands that requires you to input a **date**:

If the bot returns you this response:
```
Your format is correct, however we cannot perform the query to your Google Account
```
Then these cases may occur:

Case 1: You have problems with your API keys

Case 2: You entered a bad date, for instance your end time is earlier than your start time (Your event starts at 5 p.m. but ends at 4 p.m.)

For these two cases, you may want to resolve your API problem and run the **/addevent** again and give the bot a reasonable time interval.

### Information 2

If the bot responds in this following manner:
```
Cannot access the course
```
This problem can be caused by these following cases:

Case 1: You may have problems with your browser driver, for instance you may have a problem with your chromedriver for Google Chrome.

Case 2: You may have entered a course code that **does not exist**

### Information 3

Take note that the command **/addfirstweek** can only accept a **Monday** as the start of the first week and first recess week. 
Check if you have inputted a **Monday** and no other day for the start of the first week and first recess week as a mistake here can lead to errors in the consequent commands such as **/addcourse**.

### Information 4

Whenever a keyboard is displayed for you to click, make sure you click on them only **once** . Clicking the keyboard more than once will result in an error in your database and the bot may not be able to run properly.

**Do not** scroll up and click on previous keyboard once you are done with that specific command. This can result in an error in your database and the bot may not be able to run properly.
