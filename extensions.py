import requests
import json

from config import keys
from exceptions import APIException


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # quote - валюта, base - в какую валюту переводим quote, amount - количество валюты quote. Все принимают строку.

        # Передаем введенные пользователем данные в запрос с помощью тикеров с ключами:
        quote_ticker = keys[quote]
        base_ticker = keys[base]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # Загружаем контент в json и умножаем полученный курс валюты на введенное пользователем количество:
        total_base = json.loads(r.content)[keys[base]]
        result = float(total_base) * float(amount)

        return result
