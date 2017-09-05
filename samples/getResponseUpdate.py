import telepot
from pprint import pprint

token = "<token>"
bot = telepot.Bot(token)

response = bot.getUpdates()
pprint(response)
