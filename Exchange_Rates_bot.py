import telebot

bot = telebot.TeleBot("954169124:AAGfQJtCY2zWpFnn8qahxV8zi7UYDHodYuw")

@bot.message_handler(commands=["start"])
def start_message(mes):
    bot.send_message(mes.chat.id, "Здарова!")

@bot.message_handler(content_types=["text"])
def send_text(mes):
    if mes.text.lower() == "привет":
        bot.send_message(mes.chat.id, "Привет, чепыга!")
    elif mes.text.lower() == "здравствуй":
        bot.send_message(mes.chat.id, "Приветствую, Вас, глубоко уважаемый!")
    else:
        bot.send_message(mes.chat.id, "Чё ты там вякнул? Я не расслышал!")
    
    
bot.polling()
