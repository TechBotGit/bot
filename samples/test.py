import telepot
import os
import sys

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'
f = open(path_file, "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

print(bot.getMe())

