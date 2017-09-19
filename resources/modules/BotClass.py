import os
import sys
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import GoogleapiClass as gc
import HelperClass as hc


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
    
    @property
    def db_chat(self):
        return self._db_chat

    @property
    def list_update_message(self):
        return self._list_update_message

    @db_chat.setter
    def db_chat(self, value):
        self._db_chat = value

    @list_update_message.setter
    def list_update_message(self, value):
        self._list_update_message = value
    
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

                if msg_received == '/start':
                    self.bot.sendMessage(chat_id, "Hi! I'm a bot that tells you your course schedule and plan your meetings! Feel free to ask me stuff :)")
                    self.bot.sendMessage(chat_id, "If you want to know your course schedule, type in Course. If you want to plan your meetings, type in Meetings. If you want to know anything about me, just type in whatever you want and hope I understand :)")
                
                elif msg_received == '/createevent':
                    msg_reply = "Okay send me the details in following format:"
                    str_format = "Event Name;location;yyyy-mm-ddThh:mm:ss;yyyy-mm-ddThh:mm:ss"
                    self.bot.sendMessage(chat_id, msg_reply)
                    self.bot.sendMessage(chat_id, str_format)
                    print(response)

                elif msg_received == '/addindex':
                    msg_reply = "Sure thing. Please type your details in following format: \n"
                    str_format = "Course Name;Course Type(Full/Part Time);Index Number"
                    self.bot.sendMessage(chat_id, msg_reply)
                    self.bot.sendMessage(chat_id, str_format)
                    print(response)
                    
                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")

                elif msg_received == '/isfree':
                    self.bot.sendMessage(chat_id, "Please enter the date interval using the following format: ")
                    self.bot.sendMessage(chat_id, "YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM")
                
                elif msg_received == '/scheduleindex':
                    self.bot.sendMessage(chat_id, "Please Enter your index using the following format: ")
                    self.bot.sendMessage(chat_id, "CourseCode;Location;LAB/LEC/TUT;start_time;end_time;first_recess_week, fist_week")
                    self.bot.sendMessage(chat_id, 'For example: ')
                    self.bot.sendMessage(chat_id, 'CZ1005;HWLAB3;LAB;14:30:00;16:30:00;2017-10-2;2017-8-14')

                else:
                    self.bot.sendMessage(chat_id, "Command not updated!")

            else:
                
                # Execute the command further
                # Create the Command Object first
                BotCommandObject = BotCommand(msg['text'])
                
                # This checks if the last msg['text'] is indeed a command
                if len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/createevent':
                    
                    try:
                        BotCommandObject.CreateEventCommand()
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot create event! Make sure to enter the correct format!')
                    
                    else:
                        self.bot.sendMessage(chat_id, 'Successful!')
                
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
                
                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/addindex':
                    
                    self.bot.sendMessage(chat_id, 'Please wait while we process your information. This may take around a minute.\n')
                    self.bot.sendMessage(chat_id, 'To prevent crashing, please wait until the Success message has appeared.\n')
                    try:
                        BotCommand(msg['text']).AddIndexCommand()
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot add index! Make sure you have entered the correct format!')

                    else:
                        self.bot.sendMessage(chat_id, "Successfully added! :)")
                        #BotCommand(msg['text']).AddIndexCommand() #debug purpose

                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/scheduleindex':
                    try:
                        BotCommandObject.ScheduleIndexCommand()
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot schedule index! Make sure you have entered the correct format!')

                    else:
                        self.bot.sendMessage(chat_id, "Successfully added! :)")
                
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
            '/createevent',
            '/mergeevent',
            '/isfree',
            '/scheduleindex',
            '/quit'
        ]
        self.str_text = str_text
        
        # Updatable
        self._start_busy = None
        self._end_busy = None

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
        end_date = str_input.end_date
        # Call the GoogleAPI class and create event
        gc.GoogleAPI().createEvent(event_name, location, start_date, end_date)

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

    def AddIndexCommand(self):
        str_input = hc.StringParseIndex(self.str_text)
        str_input.Parse()
        course_name = str_input.course_name
        course_type = str_input.course_type
        index = str_input.index
        hc.splintergetdata().start(course_name, course_type, index)

    def ScheduleIndexCommand(self):
        str_input = hc.StringParseGoogleAPI(self.str_text)
        str_input.ParseIndexInput()
        
        course_code = str_input.course_code
        location_course = str_input.location_course
        class_type = str_input.class_type
        start_time = str_input.start_time
        end_time = str_input.end_time
        first_recess_week = str_input.first_recess_week
        first_week = str_input.first_week

        gc.GoogleAPI().CreateEventIndex(course_code, location_course, class_type, start_time, end_time, first_recess_week, first_week)
