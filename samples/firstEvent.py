import sys
import time
import telepot
from telepot.loop import MessageLoop
import splinter
import os
sys.path.append('../resources/modules')
import BotClass as bc


bot = bc.API().bot  # the bot object
handle = bc.API().handleAPI  # APIhandler

MessageLoop(bot, handle).run_as_thread()
print("Listening...")

# Keep the program running.
while 1:
    time.sleep(10)
