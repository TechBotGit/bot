import telepot
f = open("a.txt", "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

print(bot.getMe())
