import telepot
from pprint import pprint

f = open("a.txt", "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

response = bot.getUpdates()
pprint(response)
