import telepot


f = open("a.txt", "r")
token = (f.read())
f.close()
bot = telepot.Bot(token)

bot.sendMessage('<chat_id>', "Hi this is a message from the terminal")
