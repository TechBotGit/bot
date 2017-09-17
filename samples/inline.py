import os
import sys
import os
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
a = ['a', 'b', 'c', 'd']


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #  tuples=tuple(listofsem)
    inlines_keyboard = [[]]
    for i in range(0, len(a)):
        print(a[i])
        inlines_keyboard.append([InlineKeyboardButton(text=a[i], callback_data=a[i])])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
    bot.sendMessage(chat_id, 's', reply_markup=keyboard)
    print(type(keyboard))


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Got it')

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'
f = open(path_file, "r")
token = (f.read())
f.close()
<<<<<<< HEAD
# f=open("a.txt","r")
# TOKEN= (f.read())
# f.close()
# get token from txt
bot = telepot.Bot(token)
MessageLoop(bot, {'chat': on_chat_message,'callback_query': on_callback_query}).run_as_thread()
=======
bot = telepot.Bot(token)
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

>>>>>>> 1ea44c9a5b55daa122eb4ba96aed9f0fc1758282
print('Listening ...')
while 1:
    time.sleep(10)
