# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import django
import telebot
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intergalactic.settings")
django.setup()

from mainapp.models import Article
from usersapp.models import GeekHubUser
from telegramapp.models import TelegramUsers

token = '1821843720:AAGUfJeKRL9xky5yYYN5D08OPzTzCslUJ1M'

def main_bot(tok):
    bot = telebot.TeleBot(tok)

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('топ автор', 'топ статья', 'подписка')
    password_button = []
    otvet = telebot.types.InlineKeyboardMarkup(row_width=2)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        print(message.chat.id)
        bot.send_message(message.chat.id, f"Привет!!! {message.from_user.first_name}", reply_markup=keyboard)

    # @bot.callback_query_handler(func=lambda call: True)
    # def callback_inline(call):
    #     try:
    #         if call.message:
    #             for item in range(0, len(valute_code)):
    #                 if call.data == valute_code[item]:
    #                     bot.send_message(call.message.chat.id, courses(valute_code=valute_code[item]))
    #     except Exception as e:
    #         print(repr(e))

    @bot.message_handler(content_types=["text"])
    def commands(message):
        if message.text.lower() == "топ автор":
            users = GeekHubUser.objects.all()
            bot.send_message(message.chat.id, str(users.count()))

        if message.text.lower() == "топ статья":
            users = Article.objects.all()
            bot.send_message(message.chat.id, str(users.count()))

        if message.text.lower() == "подписка":
            registered_users = TelegramUsers.objects.filter(users_id=message.chat.id)
            print(registered_users)
            if not registered_users:
                users = TelegramUsers(users_id=message.chat.id)
                users.save()
                bot.send_message(message.chat.id, "Вы успешно подписаны на наши новости")
            else:
                bot.send_message(message.chat.id, "Ёпта! Да Вы уже подписаны на наши новости!!!")


    bot.polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_bot(token)
