# -*- coding: utf-8 -*-
import telebot
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime


def log(func):
    def wrapper(*args, **kwargs):
        t = datetime.now()
        f = func(*args, **kwargs)
        with open(f'{func.__name__}.log', 'a') as file:
           print(f, "---", t, file=file)
        return f
    return wrapper


class Currency:
    EUR_UAH = "https://www.google.com/search?q=euro+uah&oq=eur&aqs=chrome.0.69i59j69i57j46j0l2j69i65l2j69i61.1764j0j7&sourceid=chrome&ie=UTF-8"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    current_converted_price = 0
    difference = 0.5  # Разница, после которой будет отправлено сообщение об изменении курса

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    # Получает из сайта обменника строку с текущим курсом

    @log
    def get_currency_price(self):
        full_page = requests.get(self.EUR_UAH, headers=self.headers)
        soup = BeautifulSoup(full_page.content, "html.parser")
        convert = soup.findAll("span", {"class": "DFlfde SwHCTb"})
        return convert[0].text
    
    # Превращает строку из get_currency_price() в число (курс) и сравнивает с курсом на момент запуска программы

    @log
    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            return f"Курс ВЫРОС на {round(self.current_converted_price - currency, 2)} и состовляет: {currency} гривен."
        elif currency <= self.current_converted_price - self.difference:
            return f"Курс УПАЛ на {round(currency - self.current_converted_price, 2)} и состовляет: {currency} гривен."
        self.current_converted_price = currency
        #sleep(1)
        self.check_currency()
   
    def check_now(self):
        currency = float(self.get_currency_price().replace(",", "."))
        return f"Сейчас 1 евро = {currency} гривен.\nКогда курс изменится, я Вас уведомлю."

        

bot = telebot.TeleBot("секретный код")
keyboard1 = telebot.types.ReplyKeyboardMarkup(True).row("EUR/UAH")
curr = Currency()


@bot.message_handler(commands=["start"])
def start_message(mes):
    bot.send_message(mes.chat.id, "Привет, юзер!\nЭтот бот поможет тебе следить за курсом валют.", reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def start_programm(mes):
    if mes.text == "EUR/UAH":
        bot.send_message(mes.chat.id, curr.check_now())
        while True:
            try:
                bot.send_message(mes.chat.id, curr.check_currency())
            except IndexError:
                bot.send_message(mes.chat.id, "Проблемы с соединением!\nНе беспокойтесь!\nБот автоматически перезагрузится после восстановления соединения.")


bot.polling()
