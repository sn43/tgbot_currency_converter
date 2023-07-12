import requests
import json
import telebot

from config import TOKEN, keys
from exceptions import UserError


bot = telebot.TeleBot(token=TOKEN)


if __name__ == '__main__':
    @bot.message_handler()
    def test(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'I am working')

    bot.polling(none_stop=True)
