import telepot
from pprint import pprint

token = "411692236:AAFT7dtWSr_FM56juxyneZmoqPZD_qqxhR0"
bot = telepot.Bot(token)

response = bot.getUpdates()
pprint(response)
