import telepot

token = "our token"
user_id = "our id"


bot = telepot.Bot(token)

bot.sendMessage(user_id, "Hello, I'm your new bot")
