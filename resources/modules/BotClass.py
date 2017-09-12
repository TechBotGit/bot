import sys
import os
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class API(object):
    """API Basic initialisation"""
    def __init__(self):
        self.cwd = os.path.dirname(sys.argv[0])
        self.api_key = self.cwd + '/a.txt'
        f = open(self.api_key, 'r')
        self.token = f.read()
        f.close()
        self.bot = telepot.Bot(self.token)

    def handleAPI(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)  # debug msg received

        if content_type == 'text':
           
            # Convert the message to lower case
            msg_received = msg['text'].lower()
            
            # If the message is a valid command
            if BotCommand().isValidCommand(msg_received):
                if msg_received == '/start':
                    #self.bot.sendMessage(chat_id, "Beep. You can start chatting with me now, or ask me to do stuff. :)")
                    self.bot.sendMessage(chat_id, "Hi! I'm a bot that tells you your course schedule and plan your meetings! Feel free to ask me stuff :)")
                    self.bot.sendMessage(chat_id,"If you want to know your course schedule, type in Course. If you want to plan your meetings, type in Meetings. If you want to know anything about me, just type in whatever you want and hope I understand :)")
                
                elif msg_received == '/createevent':
                    self.bot.sendMessage(chat_id, "Okay send me the details in the format EventName, dd/mm/yy:hh:mm - dd/mm/yy/:hh:mm")

                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")
        
                else:
                    self.bot.sendMessage(chat_id, "Command not updated!")

            else:
                
                #manual emoticons ONLY :p
                if msg_received[0]==':':
                    if len(msg_received)<=3:
                        self.bot.sendMessage(chat_id,msg['text'])
                    else:
                        self.bot.sendMessage(chat_id,"What is that??? .-.")
                elif msg_received.find('rude')!= -1 : #had to do this elif :'(
                    self.bot.sendMessage(chat_id,BotReply().reply_dict['rude'])
                # If the bot knows reply the message
                elif BotReply().isValidtoReply(msg_received):
                    print(BotReply().reply_dict[msg_received])

                    # With name?
                    if BotReply().isWithName(msg_received):
                        self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received]+', ' + msg['chat']['first_name']+' !')
                                       
                    elif msg_received=='meetings':
                        self.bot.sendMessage(chat_id,BotReply().reply_dict[msg_received])
                        inlines_keyboard=[[]]
                        for i in range(len(PreformattedBotInlineMarkup().days)) :
                            #print(days[i])
                            inlines_keyboard.append([InlineKeyboardButton(text=PreformattedBotInlineMarkup().days[i],callbackquery=PreformattedBotInlineMarkup().days[i])])
                        keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                        self.bot.sendMessage(chat_id, 'Choose a day!', reply_markup=keyboard)
                    else:
                        self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                else:
                    self.bot.sendMessage(chat_id, "Sorry, I don't know what to reply such conversation yet. :'(")


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
            'where are you from?':'I was made at NTU Singapore :) Pretty cool isnt it?',
            'where are you from':'I was made at NTU Singapore :) Pretty cool isnt it?',
            'how old are you?':'I was made sometime in early September 2017',
            'how old are you':'I was made sometime in early September 2017',
            'what are you doing?':'Replying you. Duh.',
            'what are you doing':'Replying you. Duh.',
            'what are you?':"i'm a bot :))",
            'what are you':"i'm a bot :))",
            'what do you do?':'type in /start to know :)',
            'what do you do':'type in /start to know :)',
            'who are you?':"i'm a bot :))",
            'who are you':"i'm a bot :))",
            'thanks':'no problem!',
            'oh thanks':'no problem!',
            'ok thanks':'no problem!',
            'rude':'sry :(',
            "what's your name":'not sure hahah sry call me bot',
            "what's your name?":'not sure hahah sry call me bot',
            "what is your name?":'not sure hahah sry call me bot',
            "what is your name":'not sure hahah sry call me bot',
            'hey bot':'yep?',
            'im bored':"I'm not sure I can help you with that. Sorry :(",
            "i'm bored":"I'm not sure I can help you with that. Sorry :(",
            'course':"Feeling productive are we? Okay, let's get started",
            'meetings':"Feeling productive are we? Okay, let's get started",
        }
        #  dictionary is O(1), list is O(n), hence better use dictionary(much more faster when n is big)
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
            '/quit'
        ]

    def isValidCommand(self, command):
        return command in self.command_list

class PreformattedBotInlineMarkup(API):
    """This is a class for storing future fixed KeyboardMarkup"""
    def __init__(self):
        super().__init__()
        self.days = [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        ]
