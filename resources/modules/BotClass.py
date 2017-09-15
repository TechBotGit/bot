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
        self.db_chat = {}
        self.list_update_message = []

    def handleAPI(self, msg):
        content_type, self.chat_type, chat_id = telepot.glance(msg)
        print(content_type, self.chat_type, chat_id)  # debug msg received
        response = self.bot.getUpdates()
        self.StoreChat(response)

        if content_type == 'text':

            # Convert the message to lower case
            msg_received = msg['text'].lower()
            print(msg_received)

            # If the message is a valid command
            if BotCommand().isValidCommand(msg_received):

                if msg_received == '/start':
                    self.bot.sendMessage(chat_id, "Hi! I'm a bot that tells you your course schedule and plan your meetings! Feel free to ask me stuff :)")
                    self.bot.sendMessage(chat_id, "If you want to know your course schedule, type in Course. If you want to plan your meetings, type in Meetings. If you want to know anything about me, just type in whatever you want and hope I understand :)")
                
                elif msg_received == '/createevent':
                    msg_reply = "Okay send me the details in following format:"
                    str_format = "Event Name;location;yyyy-mm-ddThh:mm;yyyy-mm-ddThh:mm"
                    self.bot.sendMessage(chat_id, msg_reply)
                    self.bot.sendMessage(chat_id, str_format)
                    print(response)

                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")

                elif msg_received == '/isfree':
                    self.bot.sendMessage(chat_id, "Please enter the date interval using the following format: ")
                    self.bot.sendMessage(chat_id, "YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM")
                
                else:
                    self.bot.sendMessage(chat_id, "Command not updated!")

            else:
                
                # Execute the command further
                # This checks if the last msg['text'] is indeed a command

                if self.list_update_message[len(self.list_update_message) - 2] == '/createevent':
                    
                    try:
                        BotCommand().CreateEventCommand(msg['text'])
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot create event! Make sure to enter the correct format!')
                    
                    else:
                        self.bot.sendMessage(chat_id, 'Successful!')
                
                elif self.list_update_message[len(self.list_update_message) - 2] == '/isfree':
                    
                    try:
                        isFree = BotCommand().IsFreeCommand(msg['text'])
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot check! Make sure to enter the correct format!')
                    
                    else:
                        
                        self.bot.sendMessage(chat_id, isFree)
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
            'where are you from?': 'I was made at NTU Singapore :) Pretty cool isnt it?',
            'where are you from': 'I was made at NTU Singapore :) Pretty cool isnt it?',
            'how old are you?': 'I was made sometime in early September 2017',
            'how old are you': 'I was made sometime in early September 2017',
            'what are you doing?': 'Replying you. Duh.',
            'what are you doing': 'Replying you. Duh.',
            'what are you?': 'i\'m a bot :))',
            'what are you': "i'm a bot :))",
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

    def __init__(self):
        super().__init__()
        self.command_list = [
            '/start',
            '/createevent',
            '/mergeevent',
            '/isfree',
            '/quit'
        ]

    def isValidCommand(self, command):
        return command in self.command_list

    def CreateEventCommand(self, str_text):
        str_input = hc.StringParse(str_text)
        str_input.ParseEvent()
        event_name = str_input.event_name
        location = str_input.location
        start_date = str_input.start_date
        end_date = str_input.end_date

        # Call the GoogleAPI class and create event
        gc.GoogleAPI().createEvent(event_name, location, start_date, end_date)

    def IsFreeCommand(self, str_text):
        str_input = hc.StringParse(str_text)
        str_input.ParseDateRange()
        start_date_query = str_input.start_date
        end_date_query = str_input.end_date

        # Call the GoogleAPI class and check isFree
        query = gc.GoogleAPI().FreeBusyQuery(start_date_query, end_date_query)
        return gc.GoogleAPI().isFree(query)
