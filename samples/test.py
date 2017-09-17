import telepot
import os
import sys

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'

with open(path_file, 'r') as f:
	token = (f.read())

bot = telepot.Bot(token)

print(bot.getMe())
