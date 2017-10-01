import os
import sys
import json
import telepot
import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Custom Class
import GoogleapiClass as gc
import HelperClass as hc
import DBClass as db


class API(object):
    """API Basic initialisation"""
    def __init__(self):
        # Deploy Bot
        self.cwd = os.path.dirname(sys.argv[0])
        self.api_key = self.cwd + '/../resources/token.txt'
        f = open(self.api_key, 'r')
        self.token = f.read()
        f.close()
        self.bot = telepot.Bot(self.token)
        
        # Important storage information
        self._db_chat = {}
        self._list_update_message = []
        
        # additional information for course codes and indexes
        self._indexchosen = ''
        self._parseddataindex = [[],[],[],[],[],[],[]]

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
                    self.bot.sendMessage(chat_id, "Hi! Need help to be more productive? Good news, I'm here to manage your time! Feel free to ask me stuff :)")
                    self.bot.sendMessage(chat_id, "Want to add course index? Just run /addindex.")
                    self.bot.sendMessage(chat_id, "Want to plan your meetings? Just type in 'meetings' and let me schedule it for you.")
                    self.bot.sendMessage(chat_id, "Want to know me more? Just ask me whatever you want and hope I can understand :)")
                    self.bot.sendMessage(chat_id, "To know more commands just type forward slash '/' to see what's available")
                
                elif msg_received == '/createevent':
                    msg_reply = "Okay send me the details in following format:"
                    str_format = "Event Name;location;YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM"
                    self.bot.sendMessage(chat_id, msg_reply)
                    self.bot.sendMessage(chat_id, str_format)
                    self.bot.sendMessage(chat_id, "For example: Party;NTU;2017-10-08 20:00;2017-10-08 22:00")
                    print(response)
                
                elif msg_received == '/deleteevent':
                    self.bot.sendMessage(chat_id, "Sure thing. Please tell me your event ID:")

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
                        self.error = 0  # no error occured
                
                elif msg_received == '/removeindex':
                    self.bot.sendMessage(chat_id, "Please type the course code that you want to remove!")

                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")

                elif msg_received == '/isfree':
                    self.bot.sendMessage(chat_id, "Please enter the date interval using the following format: ")
                    self.bot.sendMessage(chat_id, "YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM")
                
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
                global BotCommandObject
                BotCommandObject = BotCommand(msg['text'])
                # to prevent crashing as it separates the variables so literally it can run parallelly
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
                        self.bot.sendMessage(chat_id, 'Cannot create event! You have another event on ' + start_busy + ' until ' + end_busy + ' !')
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot create event! Please try again')
                    # prevents crashing  of the full program as it limits the crash to this fuction only
                    else:
                        self.bot.sendMessage(chat_id, 'Successful! Your event ID is ' + trial[3] + '.\n Please refer to this Event ID for further information.')
                    # for debugging
                    # iso = BotCommandObject.CreateEventCommand()
                
                elif len(self.list_update_message) >= 2 and (self.list_update_message[-2] == '/deleteevent'):
                    
                    try:
                        BotCommandObject.DeleteEventCommand()
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Error occured! Have you entered the correct event ID?')
                    
                    else:
                        self.bot.sendMessage(chat_id, 'Successful!')

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
                        self.parseddataindex = BotCommandObject.parseddataindex
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot access the course! Make sure you have entered the correct format!')

                    else:
                        if not self.error:
                            self.bot.sendMessage(chat_id, "The indexes for this course code has been successfully accessed. Please do the instructions above :)")

                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/removeindex':
                    
                    self.bot.sendMessage(chat_id, 'Removing index...')
                    try:
                        BotCommandObject.RemoveIndexCommand(chat_id)
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot remove index!')

                    else:
                        self.bot.sendMessage(chat_id, "The index for this course code has been removed from your Google Calendar and our database!")
                        self.bot.sendMessage(chat_id, "Run /addindex to replace your removed index, if you wish :D")

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
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received] +', ' + msg['chat']['first_name'] + ' !')
                                        
                        elif msg_received == 'meetings':
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                            inlines_keyboard = []
                            
                            for i in range(len(hc.PreformattedBotInlineMarkup().days)):
                                inlines_keyboard.append([InlineKeyboardButton(text=hc.PreformattedBotInlineMarkup().days[i], callback_data=hc.PreformattedBotInlineMarkup().days[i])])
                            keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                            self.bot.sendMessage(chat_id, 'Choose a day!', reply_markup=keyboard)
                        
                        else:
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                
                    else:
                        self.bot.sendMessage(chat_id, "Sorry, I don't know what to reply such conversation yet. :'(")

    def on_callback_query(self, msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, chat_id, query_data)
        print(query_data)
        if msg['message']['text'].find('Please choose your index below')!=-1:
            try:
                self.indexchosen=query_data
                # print(query_data)
                BotFindIndexObject=hc.chooseindex()
                BotFindIndexObject.selectindex(self.indexchosen, self.parseddataindex)
            except:
                self.bot.answerCallbackQuery(query_id, text='Error! :(')
                self.bot.sendMessage(chat_id, 'Error occured! Please try again...')
            else:
                self.bot.answerCallbackQuery(query_id, text='Index added! :)')

            BotFindIndexObject=hc.chooseindex()
            complete_data = BotFindIndexObject.selectindex(self.indexchosen, self.parseddataindex)
            course_code_dict = {
                course_code: {
                    'index':self.indexchosen,
                    'event_id': []
                }
            }
            # Check if the dictionary already exists
            db_check = db.DB()
            if db_check.isRecordExist(chat_id, course_code_event_id=True):
                data = db_check.table_query(chat_id, course_code_event_id=True)[3]
                data_dict = json.loads(data)
                course_code_dict.update(data_dict)

            if not self.error:
                # Loads the dictionary to the database
                course_code_dict_str = json.dumps(course_code_dict)
                db.DB().update(chat_id, course_code_event_id=course_code_dict_str)

                # Initialize pre requisite before adding to Google Calendar
                toGoogle = IndexToGoogle(chat_id, complete_data)
                event_list = toGoogle.get_event()
                
                try:
                    toGoogle.PreCreateEventIndex(event_list)
                except:
                    self.bot.sendMessage(chat_id, "Unknown error has occured")
                else:
                    self.bot.sendMessage(chat_id, "Nice!")
                    self.bot.sendMessage(chat_id, "%s has been added to your Google Calendar" %(query_data))
            
        else:
            self.bot.answerCallbackQuery(query_id, text='Got it :)')

    def StoreChat(self, update_object):
        update_id = update_object[0]['update_id']
        text = update_object[0]['message']['text']
        
        # A simple dictionary {update_id: 'text'}
        self.db_chat[update_id] = text

        # only the text
        self.list_update_message = list(self.db_chat.values())


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
        #  Trivia: dictionary accessing time is close to O(1), while list is O(n), hence better use dictionary when n is big, won't affect if n is small tho
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
            '/deleteevent',
            '/isfree',
            '/addfirstweek',
            '/quit'
        ]
        self.str_text = str_text
        
        # Updatable
        self._start_busy = None
        self._end_busy = None
        self.getdata = hc.splintergetdata()  # property not yet added!!!

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
        start_date_pretty = str_input.start_time_cantik
        end_date_pretty = str_input.end_time_cantik
        end_date = str_input.end_date

        query = gc.GoogleAPI().FreeBusyQuery(start_date_pretty, end_date_pretty)
        isFree = gc.GoogleAPI().isFree(query)
        # Get the query's busy info
        if not isFree:
            print("not free!")
            return (0,start_date_pretty,end_date_pretty)
            # raise ZeroDivisionError
        # Call the GoogleAPI class and create event
        current_event_id = gc.GoogleAPI().createEvent(event_name, location, start_date, end_date)
        return (1,start_date_pretty,end_date_pretty,current_event_id)

    def DeleteEventCommand(self):
        str_input = self.str_text
        gc.GoogleAPI().deleteEvent(str_input)

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
        
        global course_code  # set course_code to global!
        course_code = str_input.course_code.upper()
        # index = str_input.index
        excel = db.DB()
        student_type = excel.table_query(chat_id, student_type=True)[2]
        is_course_code_exist = excel.isRecordExist(chat_id, course_code_event_id=True)
        course_code_str = excel.table_query(chat_id, course_code_event_id=True)[3]
        
        if course_code_str is None:
            excel.update(chat_id, course_code_event_id='{}')
        course_code_str_update = excel.table_query(chat_id, course_code_event_id=True)[3]
        course_code_dict = json.loads(course_code_str_update)
        
        if not is_course_code_exist or course_code not in list(course_code_dict.keys()):
            self.getdata.start(course_code, student_type)
            self.parseddataindex=self.getdata.parsedatahml()
            inlines_keyboard = []
            for i in range(len(self.getdata.indexlist)):
                inlines_keyboard.append([InlineKeyboardButton(text=self.getdata.indexlist[i], callback_data=self.getdata.indexlist[i])])

            keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
            self.bot.sendMessage(chat_id, 'Please choose your index below.\n Click only one of them once!', reply_markup=keyboard)
        else:
            API.error = 1
            self.bot.sendMessage(chat_id, 'Our database shows that you have already added the course code %s' %(course_code))
            self.bot.sendMessage(chat_id, 'You cannot add the same course code twice!')
            self.bot.sendMessage(chat_id, 'To change index, you must remove current existing course code by running /removeindex!')

    def RemoveIndexCommand(self, chat_id):
        course_code = self.str_text.upper()
        print(course_code)
        
        check_db = db.DB()
        course_code_db_str = check_db.table_query(chat_id, course_code_event_id=course_code)[3]
        course_code_db_obj = json.loads(course_code_db_str)

        # Remove it from Google Calendar
        Google = gc.GoogleAPI()
        try:
            for evt_id in course_code_db_obj[course_code]['event_id']:
                Google.deleteEvent(evt_id)
        except:
            self.error = 1
            raise ValueError
        
        # Remove it from the database
        if not self.error:
            del(course_code_db_obj[course_code])
            updated_course_code_str = json.dumps(course_code_db_obj)
            check_db.update(chat_id, course_code_event_id=updated_course_code_str)

    def SetTypeStudent(self, chat_id):
        str_input = hc.StringParseStudentType(self.str_text)
        str_input.ParseInput()
        # print(self.str_text)
        course_type = str_input.course_type
        print(course_type)
        excel = db.DB()
        excel.update(chat_id, student_type=course_type)

    def AddFirstWeek(self, chat_id):
        first_week, first_recess_week = self.str_text.split(';')
        
        # Initialize db
        excel = db.DB()
        # Update the exel file
        excel.update(chat_id, first_week=first_week, first_recess_week=first_recess_week)
    

class IndexToGoogle(API):
    """Description: the main class to integrate indexes with Google Calendar"""
    def __init__(self, chat_id, index_dictionary):
        super().__init__()
        self.index_dictionary = index_dictionary
        self.chat_id = chat_id
    
    def get_event(self):
        """Description: Get each a list event data from the parsed HTML
        Return: list
        """
        value_list = list(self.index_dictionary.values())
        key_list = list(self.index_dictionary.keys())
        event_list = [[] for event in range(len(value_list[0]))]  # initialize list of lists
        ParseObject = hc.StringParseGoogleAPI(self.index_dictionary)
        for i in range(len(value_list[0])):
            # Change the time format
            time = self.index_dictionary['time'][i]
            formated_time = ParseObject.ParseDateIndex(time)
            self.index_dictionary['time'][i] = formated_time

            # Change the day format
            day = self.index_dictionary['day'][i]
            # Setting the value
            ParseObject.day = day
            # Assign it to the list
            self.index_dictionary['day'][i] = ParseObject.day
            for key in key_list:
                event_list[i].append(self.index_dictionary[key][i])
        return event_list

    def PreCreateEventIndex(self, evt_list):
        """Description: preparation to add the event from evt_list to Google Calendar"""
        for i in range(len(evt_list)):
            event1 = evt_list[i]
            course_index = event1[0]
            course_type = event1[1]
            course_group = event1[2]
            day = event1[3]
            start_time = event1[4][0]
            end_time = event1[4][1]
            location = event1[5]
            recurrence = event1[6]
            first_week = db.DB().table_query(self.chat_id, first_week=True)[0]
            first_recess_week = db.DB().table_query(self.chat_id, first_recess_week=True)[1]

            # Concatenate together
            event_summary = " ".join([course_code, course_type])
            event_desc = " ".join([course_index, course_group])

            ignore_first_event = False
            if day != 'MO':
                if recurrence.count('1') != 0 or recurrence != '' or recurrence.count('1') == 0:
                    ignore_first_event = True
            
            # Recurrence Parsing
            recurrenceObject = hc.StringParseGoogleAPI(recurrence)
            recurrence_string = recurrenceObject.ParseOccurIgnoreWeek(first_week, start_time)
            
            # CreateEventIndex
            gc.GoogleAPI().CreateEventIndex(self.chat_id, event_summary, location, event_desc, start_time, end_time, first_week, first_recess_week, recurrence_string, day, ignore_first_event)
