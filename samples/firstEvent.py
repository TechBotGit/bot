import sys
import time
import telepot
from telepot.loop import MessageLoop
# import splinter
import os
sys.path.append('../resources/modules')
import BotCommand as bc

reply_dict = {
    'hi': 'Hi',
    'hello': 'Hello',
    'good morning': 'Good morning',
    'good afternoon': 'Good afternoon',
    'good evening': 'Good evening',
    'good night': 'Good night',
    'good day': 'Good day',
    'create event': 'Okay send me the details in the format EventName, dd/mm/yy:hh:mm - dd/mm/yy/:hh:mm'
    }
reply_with_name = {
    'hi': 1,
    'hello': 1,
    'good morning': 1,
    'good afternoon': 1,
    'good evening': 1,
    'good night': 1,
    'good day': 1,
    'create event': 0
}


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        response = bot.getUpdates()

        msg_received = msg['text'].lower()

        if bc.BotCommand(msg_received).isValidCommand(msg_received):  # if it a command
            command_reply = bc.BotCommand(msg_received).executeCommand(msg_received)
            bot.sendMessage(chat_id, command_reply)

        else:
            if msg_received in reply_dict:
                print(reply_dict[msg_received])
                if reply_with_name[msg_received] == 1:
                    bot.sendMessage(chat_id, reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+' !')
                else:
                    bot.sendMessage(chat_id, reply_dict[msg_received])
            else:
                bot.sendMessage(chat_id, "Sorry, I don't know what to reply such conversation yet. :'( ")

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'
f = open(path_file, "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

MessageLoop(bot, handle).run_as_thread()
print("Listening...")

# Keep the program running.
while 1:
    time.sleep(10)
