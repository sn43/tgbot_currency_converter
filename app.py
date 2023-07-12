import json
import requests
import telebot

from config import TOKEN, keys
from exceptions import APIException


bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_handler(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате:' \
           '\n<Валюта> <В какую валюту перевести> <Количество валюты>' \
           '\n\n  —  название валюты вводится в единственном числе' \
           '\n  —  количество валюты указывается числом' \
           '\n  —  в качестве разделителя используйте пробел' \
           '\n\nДля просмотра списка всех доступных валют введите /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_handler(message: telebot.types.Message):
    text = 'Список доступных валют:\n'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    # quote - валюта, base - в какую валюту переводим quote, amount - количество валюты quote. Разбиваем пустой строкой:
    values = message.text.split(' ')
    quote, base, amount = values

    # Передаем введенные пользователем данные в запрос с помощью тикеров с ключами:
    quote_ticker = keys[quote]
    base_ticker = keys[base]
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    # Загружаем контент в json и умножаем полученный курс валюты на введенное пользователем количество:
    total_base = json.loads(r.content)[keys[base]]
    result = float(total_base) * float(amount)

    # Выводим пользователю сообщение с результатом:
    text = f'Цена {amount} {keys[quote]} составляет:\n{result} {keys[base]}'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':

    bot.polling(none_stop=True)
