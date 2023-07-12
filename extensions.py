import requests
import json

from config import keys
from exceptions import APIException


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # quote - валюта, base - в какую валюту переводим quote, amount - количество валюты quote. Все принимают строку.

        # Обработка исключений:
        if quote == base:
            raise APIException(f'Указана одинаковая валюта: {quote}')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Указана неверная валюта: {quote}')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Указана неверная валюта: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Недопустимое значение валюты: {amount}')

        if float(amount) <= 0:
            raise APIException(f'Количество не может быть отрицательным, либо равно нулю:\n {amount}')

        # Передаем введенные пользователем данные в запрос с помощью тикеров с ключами:
        quote_ticker = keys[quote.lower()]
        base_ticker = keys[base.lower()]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # Загружаем контент в json и умножаем полученный курс валюты на введенное пользователем количество:
        total_base = json.loads(r.content)[keys[base.lower()]]
        calc = float(total_base) * float(amount)
        result = f'Цена {amount} {keys[quote.lower()]} составляет:\n{calc} {keys[base.lower()]}'

        return result
