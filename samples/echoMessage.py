import sys
import time
import telepot
from telepot.loop import MessageLoop
import os
import sys

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

f = open(path_file, "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

MessageLoop(bot, handle).run_as_thread()
print("Listening...")

# Keep the program running.
while 1:
    time.sleep(10)
