import requests
from bs4 import BeautifulSoup
from time import sleep



class Currency:
    EUR_UAH = "https://www.google.com/search?q=euro+uah&oq=eur&aqs=chrome.0.69i59j69i57j46j0l2j69i65l2j69i61.1764j0j7&sourceid=chrome&ie=UTF-8"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    current_converted_price = 0
    difference = 0.01  # Разница, после которой будет отправлено сообщение об изменении курса

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    # Получает из сайта обменника строку с текущим курсом
    def get_currency_price(self):
        full_page = requests.get(self.EUR_UAH, headers=self.headers)
        soup = BeautifulSoup(full_page.content, "html.parser")
        convert = soup.findAll("span", {"class": "DFlfde SwHCTb"})
        return convert[0].text
    
    # Превращает строку из get_currency_price() в число (курс) и сравнивает с курсом на момент запуска программы
    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            print("Курс сильно вырос:", currency, "гривен.")
        elif currency <= self.current_converted_price - self.difference:
            print("Курс сильно упал:", currency, "гривен.")
        print("Сейчас 1 евро =", currency, "гривен.")
        self.current_converted_price = currency
        #sleep(1)
        self.check_currency()

while True:
    try:
        curr = Currency()
        curr.check_currency()
    except IndexError:
        print("Проблемы с соединением.//////////////////////////////////////////////////")
