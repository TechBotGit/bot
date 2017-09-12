import sys
import os
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'
f = open(path_file, "r")
token = (f.read())
f.close()

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

button_list = [
[KeyboardButton("col 1")],
[KeyboardButton("col 2")],
[KeyboardButton("row 2")]
]
reply_markup = ReplyKeyboardMarkup(button_list)
bot.send_message("A two-column menu", reply_markup=reply_markup)