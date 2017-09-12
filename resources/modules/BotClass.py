import sys
import os
import telepot
from telepot.loop import MessageLoop


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
                    self.bot.sendMessage(chat_id, "Beep. You can start chatting with me now, or ask me to do stuff. :)")

                elif msg_received == '/createevent':
                    self.bot.sendMessage(chat_id, "Okay send me the details in the format EventName, dd/mm/yy:hh:mm - dd/mm/yy/:hh:mm")

                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")
        
                else:
                    self.bot.sendMessage(chat_id, "Command not updated!")

            else:

                # If the bot knows reply the message
                if BotReply().isValidtoReply(msg_received):
                    print(BotReply().reply_dict[msg_received])

                    # With name?
                    if BotReply().isWithName(msg_received):
                        self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received]+', ' + msg['chat']['first_name']+' !')

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
            'hello': 'Hello',
            'good morning': 'Good morning',
            'good afternoon': 'Good afternoon',
            'good evening': 'Good evening',
            'good night': 'Good night',
            'good day': 'Good day',
        }

        self.reply_with_name = {
            'hi': 1,
            'hello': 1,
            'good morning': 1,
            'good afternoon': 1,
            'good evening': 1,
            'good night': 1,
            'good day': 1,
        }

    def isValidtoReply(self, msg):
        return msg in self.reply_dict

    def isWithName(self, msg):
        return self.reply_with_name[msg] == 1


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
