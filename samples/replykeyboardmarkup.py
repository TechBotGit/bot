import os
import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg['text'] == '/key':
            bot.sendMessage(chat_id, 'testing custom keyboard',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3")],
                                    [KeyboardButton(text="4"), KeyboardButton(text="5"), KeyboardButton(text="6")],
                                    [KeyboardButton(text="7"), KeyboardButton(text="8"), KeyboardButton(text="9")]
                                ]
                            ))


cwd = os.path.dirname(sys.argv[0])
api_key = cwd + '/a.txt'
f = open(api_key, 'r')
token = f.read()
f.close()
bot = telepot.Bot(token)
print('Listening ...')
bot.message_loop({'chat': on_chat_message}, run_forever=True)