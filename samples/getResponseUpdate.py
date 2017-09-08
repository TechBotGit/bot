import telepot
from pprint import pprint
import os
import sys

cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'

f = open(path_file, "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

response = bot.getUpdates()
pprint(response)
