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


@bot.message_handler(chat_types=['text'])
def converter(message: telebot.types.Message):
    pass


if __name__ == '__main__':

    bot.polling(none_stop=True)
