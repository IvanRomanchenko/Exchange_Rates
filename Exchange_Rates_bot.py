import telebot
import requests
from bs4 import BeautifulSoup
from time import sleep



class Currency:
    #EUR_UAH = "https://www.google.com/search?q=euro+uah&oq=eur&aqs=chrome.0.69i59j69i57j46j0l2j69i65l2j69i61.1764j0j7&sourceid=chrome&ie=UTF-8"
    EUR_UAH = "https://transferwise.com/ru/currency-converter/eur-to-uah-rate?amount=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    current_converted_price = 0
    difference = 0.01  # Разница, после которой будет отправлено сообщение об изменении курса

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    # Получает из сайта обменника строку с текущим курсом
    def get_currency_price(self):
        full_page = requests.get(self.EUR_UAH, headers=self.headers)
        soup = BeautifulSoup(full_page.content, "html.parser")
        convert = soup.findAll("span", {"class": "text-success"})
        return convert[0].text
    
    # Превращает строку из get_currency_price() в число (курс) и сравнивает с курсом на момент запуска программы
    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            return f"Курс ВЫРОС на {difference} и состовляет: {currency} гривен."
        elif currency <= self.current_converted_price - self.difference:
            return f"Курс УПАЛ на {difference} и состовляет: {currency} гривен."
        self.current_converted_price = currency
        #sleep(1)
        self.check_currency()

    def check_now(self):
        currency = float(self.get_currency_price().replace(",", "."))
        return f"Сейчас 1 евро = {currency} гривен.\nКогда курс изменится, я Вас уведомлю."

        

bot = telebot.TeleBot("954169124:AAGfQJtCY2zWpFnn8qahxV8zi7UYDHodYuw")
keyboard1 = telebot.types.ReplyKeyboardMarkup(True).row("EUR/UAH")
curr = Currency()

@bot.message_handler(commands=["start"])
def start_message(mes:str) -> str:
    bot.send_message(mes.chat.id, "Привет, юзер!\nЭтот бот поможет тебе следить за курсом валют.", reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def start_programm(mes):
    if mes.text == "EUR/UAH":
        while True:
            try:
                bot.send_message(mes.chat.id, curr.check_now())
                bot.send_message(mes.chat.id, curr.check_currency())
            except IndexError:
                bot.send_message(mes.chat.id, "Проблемы с соединением!\nНе беспокойтесь!\nБот автоматически перезагрузится после восстановления соединения.")



bot.polling()
