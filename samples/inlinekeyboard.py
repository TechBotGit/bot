import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import splinter
import os
import sys


days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #response=getUpdates()
    #tuples=tuple(listofsem)
    
        
    
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Got it')

reply_dict = {
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
second_reply = {
    'hi': 1,
    'hi bot': 1,
    'hey':1,
    'hello': 1,
    'good morning': 1,
    'good afternoon': 1,
    'good evening': 1,
    'good night': 1,
    'good day': 1,
    'who created you?': 1,
    'who created you': 1,
    'where are you from?':1,
    'where are you from':1,
    'how old are you?':1,
    'how old are you':1,
    "what is your name?":1,
    "what is your name":1,
    'what are you doing?':1,
    'what are you doing':1,
    'what are you?':1,
    "what's your name?":1,
    "what's your name":1,
    'what are you':1,
    'who are you?':1,
    'who are you':1,
    'what do you do?':1,
    'what do you do':1,
    'thanks':1,
    'oh thanks':1,
    'ok thanks':1,
    'rude':1,
    'hey bot':1,
    'im bored':1,
    "i'm bored":1,
    "course":1,
    'meetings':1,
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
            bot.sendMessage(chat_id, "Hi! I'm a bot that tells you your course schedule and plan your meetings! Feel free to ask me stuff :)")
            bot.sendMessage(chat_id,"If you want to know your course schedule, type in Course. If you want to plan your meetings, type in Meetings. If you want to know anything about me, just type in whatever you want and hope I understand :)")
        elif msg_received == 'hi':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'hi bot':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'hello':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'good morning':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'good afternoon':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'good evening':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'good night':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'good day':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received == 'hey':
            bot.sendMessage(chat_id,reply_dict[msg_received]+', ' + response[0]['message']['from']['first_name']+'!')
        elif msg_received.find('rude')!= -1 :
            bot.sendMessage(chat_id,reply_dict['rude'])
        elif msg_received=='meetings':
            bot.sendMessage(chat_id, reply_dict[msg_received])
            inlines_keyboard=[[]]
            for i in range(0,len(days)) :
                print(days[i])
                inlines_keyboard.append([InlineKeyboardButton(text=days[i], callback_data=days[i])])
            keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
            bot.sendMessage(chat_id, 'Choose a day!', reply_markup=keyboard)
        elif msg_received in reply_dict:
            print(reply_dict[msg_received])  # debug reply
            if second_reply[msg_received] == 1:
                bot.sendMessage(chat_id, reply_dict[msg_received])
        else:
            bot.sendMessage(chat_id, "Sorry, I don't know what to reply to such conversation yet. :'( ")
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