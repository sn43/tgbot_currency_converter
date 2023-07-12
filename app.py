import telebot

from config import TOKEN, keys
from extensions import Converter
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
def output(message: telebot.types.Message):
    # quote - валюта, base - в какую валюту переводим quote, amount - количество валюты quote. Разбиваем пустой строкой:
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверный формат команды.')

        quote, base, amount = values
        # Вытаскиваем результат из get_price и выводим его пользователю, если нет исключений:
        result = Converter.get_price(quote, base, amount)
    except APIException as exc:
        bot.reply_to(message, f'Ошибка ввода:\n{exc}')
    except Exception as exc:
        bot.reply_to(message, f'Ошибка сервера:\n{exc}')
    else:
        bot.send_message(message.chat.id, result)


if __name__ == '__main__':
    bot.polling(none_stop=True)
