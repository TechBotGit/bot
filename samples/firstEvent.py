import sys
import os
import time
from telepot.loop import MessageLoop

# Change the current directory
cwd = os.path.dirname(sys.argv[0])
os.chdir(cwd)
sys.path.append('../resources/modules')
import BotClass as bc


bot = bc.API().bot  # the bot object
handle = bc.API().handleAPI  # APIhandler
callbackquery = bc.API().on_callback_query

MessageLoop(bot, {'chat': handle, 'callback_query': callbackquery}).run_as_thread()
print("Listening...")

# Keep the program running.
while 1:
    time.sleep(10)
