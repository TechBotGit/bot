import telepot

# Credentials
token = "411692236:AAFT7dtWSr_FM56juxyneZmoqPZD_qqxhR0"
user_id = "200158786"


bot = telepot.Bot(token)

bot.sendMessage(user_id, "Hello, I'm your new bot")
