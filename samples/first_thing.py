import sys
import time
import telepot
from telepot.loop import MessageLoop
import splinter
import os
import sys

reply_dict = {
    'hi': 'Hi',
    'hello': 'Hello',
    'good morning': 'Good morning',
    'good afternoon': 'Good afternoon',
    'good evening': 'Good evening',
    'good night': 'Good night',
    'good day': 'Good day'
    }
second_reply = {
    'hi': 1,
    'hello': 1,
    'good morning': 1,
    'good afternoon': 1,
    'good evening': 1,
    'good night': 1,
    'good day': 1
    }


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)  # debug msg received

    if content_type == 'text':
        response = bot.getUpdates()
        print(response)  # debug id response
        # bot.sendMessage(chat_id, msg['text'])
        msg_received = msg['text'].lower()
        print(msg['text'])  # debug input
        print(msg_received)  # debug lowered input
        if msg_received == '/start':
            print("bot started")
            bot.sendMessage(chat_id, "Beep. You can start chatting with me now, or ask me to do stuff. :)")
        elif msg_received in reply_dict:
            print(reply_dict[msg_received])  # debug reply
            if second_reply[msg_received] == 1:
                bot.sendMessage(chat_id, reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+' '+response[0]['message']['from']['last_name']+'!')
            else:
                bot.sendMessage(chat_id, reply_dict[msg_received])
        else:
            bot.sendMessage(chat_id, "Sorry, I don't know what to reply such conversation yet. :'( ")
        # print(response[0]['message']['from']['first_name']+response[0]['message']['from']['last_name'])

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
