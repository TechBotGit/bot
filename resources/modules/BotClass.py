import os
import sys
import time
import telepot
import datetime
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Custom Class
import GoogleapiClass as gc
import HelperClass as hc
import DBClass as db

#for passing da object


class API(object):
    """API Basic initialisation"""
    def __init__(self):
        # Deploy Bot
        self.cwd = os.path.dirname(sys.argv[0])
        self.api_key = self.cwd + '/a.txt'
        f = open(self.api_key, 'r')
        self.token = f.read()
        f.close()
        self.bot = telepot.Bot(self.token)
        # Important storage information
        self._db_chat = {}
        self._list_update_message = []
        # additional information for index
        self._indexchosen=''
        self._parseddataindex=[[],[],[],[],[],[],[]]
        # Error raising
        self._error = 0
    
    @property
    def db_chat(self):
        return self._db_chat

    @property
    def list_update_message(self):
        return self._list_update_message

    @property
    def indexchosen(self):
        return self._indexchosen
    
    @property
    def parseddataindex(self):
        return self._parseddataindex
    
    @property
    def error(self):
        return self._error
    @db_chat.setter
    def db_chat(self, value):
        self._db_chat = value

    @list_update_message.setter
    def list_update_message(self, value):
        self._list_update_message = value

    @indexchosen.setter
    def indexchosen(self, value):
        self._indexchosen = value

    @parseddataindex.setter
    def parseddataindex(self, value):
        self._parseddataindex = value

    @error.setter
    def error(self, value):
        self._error = value
        return self._error

    def handleAPI(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)  # debug msg received
        response = self.bot.getUpdates()
        self.StoreChat(response)

        if content_type == 'text':

            # Convert the message to lower case
            msg_received = msg['text'].lower()

            # If the message is a valid command
            if BotCommand(msg_received).isValidCommand():
                # Send users a message related to the command
                if msg_received == '/start':
                    self.bot.sendMessage(chat_id, "Hi! I'm a bot that tells you your course schedule and plan your meetings! Feel free to ask me stuff :)")
                    self.bot.sendMessage(chat_id, "If you want to know your course schedule, type in Course. If you want to plan your meetings, type in Meetings. If you want to know anything about me, just type in whatever you want and hope I understand :)")
                
                elif msg_received == '/createevent':
                    msg_reply = "Okay send me the details in following format:"
                    str_format = "Event Name;location;YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM"
                    self.bot.sendMessage(chat_id, msg_reply)
                    self.bot.sendMessage(chat_id, str_format)
                    self.bot.sendMessage(chat_id, "For example: Party;NTU;2017-10-08 20:00;2017-10-08 22:00")
                    print(response)

                elif msg_received == '/setstudenttype' or msg_received == '/setstudentype' or msg_received == '/st':
                    self.bot.sendMessage(chat_id,'Are you a full time or part time student?',reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Full Time"), KeyboardButton(text="Part Time")]],one_time_keyboard=True))

                elif msg_received == '/addindex':
                    self.bot.sendMessage(chat_id,'Sure thing.\n')
                    print(response)
                    check_db = db.DB()
                    first_week_exist = check_db.isRecordExist(chat_id, first_week=True)
                    first_recess_week_exist = check_db.isRecordExist(chat_id, first_recess_week=True)
                    student_type_exist = check_db.isRecordExist(chat_id, student_type=True)
                    is_satisfied = [first_week_exist, first_recess_week_exist, student_type_exist]
                    if not all(is_satisfied):
                        # any of the requirements are not satisfied
                        self.bot.sendMessage(chat_id,'Hmm... Wait a second. You haven\'t told me what enough data!')
                        self.bot.sendMessage(chat_id,'Run /setstudenttype or /st to set your student_type, i.e. Full Time or Part Time')
                        self.bot.sendMessage(chat_id, 'Run /addfirstweek to set your first_week and first_recess_week')
                        self.error = 1  # explicitly telling that there is an error
                    else:
                        self.bot.sendMessage(chat_id, "Please type your course code below. For example, CZ1003")
                        print(response)
                        self.error = 0
                    
                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")

                elif msg_received == '/isfree':
                    self.bot.sendMessage(chat_id, "Please enter the date interval using the following format: ")
                    self.bot.sendMessage(chat_id, "YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM")
                
                elif msg_received == '/scheduleindex':
                    self.bot.sendMessage(chat_id, "Please Enter your index using the following format: ")
                    self.bot.sendMessage(chat_id, "CourseCode;Location;LAB/LEC/TUT;start_time;end_time;first_recess_week, fist_week")
                    self.bot.sendMessage(chat_id, 'For example: ')

                    self.bot.sendMessage(chat_id, 'CZ1005;HWLAB3;LAB;14:30:00;16:30:00')
                
                elif msg_received == '/addfirstweek':
                    self.bot.sendMessage(chat_id, "Please Enter your first week and first recess week using the following format: ")
                    self.bot.sendMessage(chat_id, "FirstWeek;FirstRecessWeek")
                    self.bot.sendMessage(chat_id, 'For example: ')
                    self.bot.sendMessage(chat_id, '2017-8-14;2017-10-2')
                
                else:
                    self.bot.sendMessage(chat_id, "Command not updated!")

            else:
                
                # Execute the command further
                # Create the Command Object first
                BotCommandObject = BotCommand(msg['text'])
                #to prevent crashing as it separates the variables so literally it can run parallelly
                # This checks if the last msg['text'] is indeed a command
                if len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/createevent':
                    
                    try:
                        trial = BotCommandObject.CreateEventCommand()
                        1 / trial[0]

                    except ValueError:
                        self.bot.sendMessage(chat_id, 'Cannot create event! Make sure to enter the correct format!')
                    
                    except ZeroDivisionError:
                        query = gc.GoogleAPI().FreeBusyQuery(trial[1],trial[2])
                        info_busy = gc.GoogleAPI().BusyInfo(query)
                        start_busy = info_busy[0]
                        end_busy = info_busy[1]
                        start_busy = start_busy[:19]
                        end_busy = end_busy[:19]
                        start_busy = datetime.datetime.strptime(start_busy,"%Y-%m-%dT%H:%M:%S")
                        start_busy = start_busy.strftime("%Y-%m-%d %H:%M")
                        end_busy = datetime.datetime.strptime(end_busy,"%Y-%m-%dT%H:%M:%S")
                        end_busy = end_busy.strftime("%Y-%m-%d %H:%M")
                        self.bot.sendMessage(chat_id, 'Cannot create event! You have another event on '+start_busy+' until '+end_busy+' !')
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot create event! Please try again')
                    # prevents crashing  of the full program as it limits the crash to this fuction only
                    else:
                        self.bot.sendMessage(chat_id, 'Successful!')
                    #for debugging
                    #iso = BotCommandObject.CreateEventCommand()
                
                elif len(self.list_update_message) >= 2 and (self.list_update_message[-2] == '/setstudenttype' or self.list_update_message[-2] == '/setstudentype' or self.list_update_message[-2] == '/st'):
                    
                    try:
                        BotCommandObject.SetTypeStudent(chat_id)
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Wrong format!')
                    
                    else:
                        self.bot.sendMessage(chat_id, 'Successful!',reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    # BotCommandObject.SetTypeStudent()

                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/isfree':
                    try:

                        isFree = BotCommandObject.IsFreeCommand()
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot check! Make sure to enter the correct format!')
                    
                    else:
                        self.bot.sendMessage(chat_id, isFree)
                        if isFree:
                            self.bot.sendMessage(chat_id, 'You are free on this time interval')
                        else:
                            start_busy = BotCommandObject.start_busy
                            end_busy = BotCommandObject.end_busy
                            self.bot.sendMessage(chat_id, 'You are busy on this interval!')
                            self.bot.sendMessage(chat_id, 'You have an event from %s to %s' % (start_busy, end_busy))
                
                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/addindex' and not self.error:
                    
                    self.bot.sendMessage(chat_id, 'Please wait while we process your information. This may take around a minute.\n')
                    self.bot.sendMessage(chat_id, 'To prevent crashing, please wait until the Success message has appeared.\n')
                    try:
                        self.indexchosen=''
                        BotCommandObject.AddIndexCommand(chat_id)
                        self.parseddataindex=BotCommandObject.parseddataindex
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot access the course! Make sure you have entered the correct format!')

                    else:
                        self.bot.sendMessage(chat_id, "Course code successfully accessed. Please do the instructions above :)")
                    #few lines below are for debug purpose
                    #passingobject=BotCommandObject
                    #BotCommandObject.getdata.selectindex(self.indexchosen)

                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/scheduleindex':
                    try:
                        BotCommandObject.ScheduleIndexCommand(chat_id)
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot schedule index! Make sure you have entered the correct format!')

                    else:
                        self.bot.sendMessage(chat_id, "Successfully added! :)")
                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/addfirstweek':
                    try:
                        BotCommandObject.AddFirstWeek(chat_id)
                    except:
                        self.bot.sendMessage(chat_id, "Database error!")
                    else:
                        self.bot.sendMessage(chat_id, 'Captured!')
                        self.bot.sendMessage(chat_id, 'Your data is sucessfully recorded in our database!')
                
                else:

                    # Below is not a command. It only makes the bot smarter
                    # manual emoticons ONLY :p
                    if msg_received[0] == ':':
                        
                        if len(msg_received) <= 3:
                            self.bot.sendMessage(chat_id, msg['text'])
                        
                        else:
                            self.bot.sendMessage(chat_id, "What is that??? .-.")
                    elif msg_received.find('rude') != -1:
                        self.bot.sendMessage(chat_id, BotReply().reply_dict['rude'])
                    
                    # If the bot knows reply the message
                    elif BotReply().isValidtoReply(msg_received):
                        print(BotReply().reply_dict[msg_received])

                        # With name?
                        if BotReply().isWithName(msg_received):
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received] +', ' + msg['chat']['first_name']+' !')
                                        
                        elif msg_received == 'meetings':
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                            inlines_keyboard = []
                            
                            for i in range(len(hc.PreformattedBotInlineMarkup().days)):
                                # print(hc.PreformattedBotInlineMarkup().days[i])
                                inlines_keyboard.append([InlineKeyboardButton(text=hc.PreformattedBotInlineMarkup().days[i], callback_data=hc.PreformattedBotInlineMarkup().days[i])])
                            # print(inlines_keyboard)
                            keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                            self.bot.sendMessage(chat_id, 'Choose a day!', reply_markup=keyboard)
                        
                        else:
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                
                    else:
                        self.bot.sendMessage(chat_id, "Sorry, I don't know what to reply such conversation yet. :'(")

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        print(query_data)
        if msg['message']['text'].find('Please choose your index below')!=-1:
            try:
                self.indexchosen=query_data
                #print(query_data)
                BotFindIndexObject=hc.chooseindex()
                BotFindIndexObject.selectindex(self.indexchosen, self.parseddataindex)
            except:
                self.bot.answerCallbackQuery(query_id, text='Error! :(')
                self.bot.sendMessage(from_id, 'Error occured! Please try again...')
            else:
                self.bot.answerCallbackQuery(query_id, text='Index added! :)')
            #below is for debugging only
            # self.indexchosen=query_data
            # #print(query_data)
            # BotFindIndexObject=hc.chooseindex()
            # BotFindIndexObject.selectindex(self.indexchosen, self.parseddataindex)
        else:
            self.bot.answerCallbackQuery(query_id, text='Got it :)')

    def StoreChat(self, update_object):
        update_id = update_object[0]['update_id']
        text = update_object[0]['message']['text']
        
        # A simple dictionary {update_id: 'text'}
        self.db_chat[update_id] = text

        # only the text
        self.list_update_message = list(self.db_chat.values())
#RECORDS THE CONVERSATION AND CHECKS IF YOU HAVE NOT GIVEN YOUR INPUT IT WILL DO NOTHING

class BotReply(API):
    """This is a class for Replies"""
    def __init__(self):
        super().__init__()
        self.reply_dict = {
            'hi': 'Hi',
            'hi bot': 'Hi',
            'hey': 'Hey',
            'hello': 'Hello',
            'good morning': 'Good morning',
            'good afternoon': 'Good afternoon',
            'good evening': 'Good evening',
            'good night': 'Good night',
            'good day': 'Good day',
            'who created you?': 'Awesome people named Jason, Hans, Audrey, Gaby, and Dennis :)',
            'who created you': 'Awesome people named Jason, Hans, Audrey, Gaby, and Dennis :)',
            'where are you from?': 'I was made at NTU Singapore :) Pretty cool isn\'t it?',
            'where are you from': 'I was made at NTU Singapore :) Pretty cool isn\'t it?',
            'how old are you?': 'I was made sometime in early September 2017',
            'how old are you': 'I was made sometime in early September 2017',
            'what are you doing?': 'Replying you. Duh.',
            'what are you doing': 'Replying you. Duh.',
            'what are you?': 'I\'m a bot :))',
            'what are you': "I'm a bot :))",
            'what do you do?': 'type in /start to know :)',
            'what do you do': 'type in /start to know :)',
            'who are you?': "i'm a bot :))",
            'who are you': "i'm a bot :))",
            'thanks': 'no problem!',
            'oh thanks': 'no problem!',
            'ok thanks': 'no problem!',
            'rude': 'sry :(',
            "what's your name": "not sure hahah sry call me bot",
            "what's your name?": "not sure hahah sry call me bot",
            "what is your name?": "not sure hahah sry call me bot",
            "what is your name": "not sure hahah sry call me bot",
            'hey bot': "yep?",
            'im bored': "I'm not sure I can help you with that. Sorry :(",
            "i'm bored": "I'm not sure I can help you with that. Sorry :(",
            'course': "Feeling productive are we? Okay, let's get started",
            'meetings': "Feeling productive are we? Okay, let's get started",
        }
        #  Trivia: dictionary accessing time is close to O(1), while list is O(n), 
        #  hence better use dictionary when n is big, won't affect if n is small tho
        self.reply_with_name = [
            'hi',
            'hi bot',
            'hey',
            'hello',
            'good morning',
            'good afternoon',
            'good evening',
            'good night',
            'good day',
        ]

    def isValidtoReply(self, msg):
        return msg in self.reply_dict

    def isWithName(self, msg):
        return msg in self.reply_with_name


class BotCommand(API):
    """This is a class for Commands"""
    
    def __init__(self, str_text):
        super().__init__()
        self.command_list = [
            '/start',
            '/addindex',
            '/removeindex',
            '/setstudenttype',
            '/st',
            '/setstudentype',
            '/createevent',
            '/isfree',
            '/scheduleindex',
            '/addfirstweek',
            '/quit'
        ]
        self.str_text = str_text
        
        # Updatable
        self._start_busy = None
        self._end_busy = None
        self.getdata = hc.splintergetdata()#property not yet added!!!

    @property
    def start_busy(self):
        return self._start_busy

    @property
    def end_busy(self):
        return self._end_busy

    @start_busy.setter
    def start_busy(self, value):
        self._start_busy = value

    @end_busy.setter
    def end_busy(self, value):
        self._end_busy = value
    
    def isValidCommand(self):
        return self.str_text in self.command_list

    def CreateEventCommand(self):
        str_input = hc.StringParseGoogleAPI(self.str_text)
        str_input.ParseEvent()
        event_name = str_input.event_name
        location = str_input.location
        start_date = str_input.start_date
        start_date_pretty = str_input._start_time_cantik
        end_date_pretty = str_input._end_time_cantik
        end_date = str_input.end_date
        #print("beep",start_date_pretty,end_date_pretty)
        query = gc.GoogleAPI().FreeBusyQuery(start_date_pretty, end_date_pretty)
        isFree = gc.GoogleAPI().isFree(query)
        # Get the query's busy info
        if not isFree:
            print("not free!")
            return (0,start_date_pretty,end_date_pretty)
            #raise ZeroDivisionError
        # Call the GoogleAPI class and create event
        gc.GoogleAPI().createEvent(event_name, location, start_date, end_date)
        return (1,start_date_pretty,end_date_pretty)

    def IsFreeCommand(self):
        str_input = hc.StringParseGoogleAPI(self.str_text)
        str_input.ParseDateRange()
        start_date_query = str_input.start_date
        end_date_query = str_input.end_date

        # Call the GoogleAPI class and check isFree
        query = gc.GoogleAPI().FreeBusyQuery(start_date_query, end_date_query)

        isFree = gc.GoogleAPI().isFree(query)
        # Get the query's busy info
        if not isFree:
            info_busy = gc.GoogleAPI().BusyInfo(query)
            self.start_busy = info_busy[0]
            self.end_busy = info_busy[1]
        return isFree

    def AddIndexCommand(self,chat_id):
        str_input = hc.StringParseIndex(self.str_text)
        str_input.Parse()
        course_name = str_input.course_name
        index = str_input.index
        excel = db.DB()
        student_type = excel.table_query(chat_id, student_type=True)[2]
        self.getdata.start(course_name, student_type)
        self.parseddataindex=self.getdata.parsedatahml()
        inlines_keyboard = []
        for i in range(len(self.getdata.indexlist)):
            # print(hc.PreformattedBotInlineMarkup().days[i])
            inlines_keyboard.append([InlineKeyboardButton(text=self.getdata.indexlist[i], callback_data=self.getdata.indexlist[i])])
        # print(inlines_keyboard)
        keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
        self.bot.sendMessage(chat_id, 'Please choose your index below.\n Click only one of them once!', reply_markup=keyboard)

    def SetTypeStudent(self, chat_id):
        str_input = hc.StringParseStudentType(self.str_text)
        str_input.ParseInput()
        # print(self.str_text)
        course_type = str_input.course_type
        print(course_type)
        excel = db.DB()
        excel.update(chat_id, student_type=course_type)
        
    def ScheduleIndexCommand(self, chat_id):
        str_input = hc.StringParseGoogleAPI(self.str_text)
        str_input.ParseIndexInput()
        
        course_code = str_input.course_code
        location_course = str_input.location_course
        class_type = str_input.class_type
        start_time = str_input.start_time
        end_time = str_input.end_time
        
        first_week = db.DB().table_query(chat_id, first_week=True)[0]
        first_recess_week = db.DB().table_query(chat_id, first_recess_week=True)[1]

        gc.GoogleAPI().CreateEventIndex(course_code, location_course, class_type, start_time, end_time, first_week, first_recess_week)

    def AddFirstWeek(self, chat_id):
        first_week, first_recess_week = self.str_text.split(';')
        
        # Initialize db
        excel = db.DB()
        # Update the exel file
        excel.update(chat_id, first_week=first_week, first_recess_week=first_recess_week)
