# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import django
import telebot
from email.utils import parseaddr

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intergalactic.settings")
django.setup()

from mainapp.models import Article
from usersapp.models import GeekHubUser
from telegramapp.models import TelegramUsers
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

token = '1821843720:AAGUfJeKRL9xky5yYYN5D08OPzTzCslUJ1M'

action = ['Да', 'Нет']


def main(request, verify):
    try:
        verify_data = verify.split(':')
        if len(verify_data) == 2:
            user_account = GeekHubUser.objects.get(email=verify_data[1])
            if user_account:
                user_account.telegram = verify_data[0]
                user_account.save()
                context = {'msg': 'Поздравляем, вы успешно привязали свою учетную запись Telegram'}
        else:
            context = {'msg': 'Чё то ты темнишь бро!'}
    except Exception as e:
        context = {'msg': f'Слыш, тут херня какая то образовалась: {e}, я в душе не .... чё это!'}

    return render(request, 'usersapp/verification_telegram.html', context)


def main_bot(tok):
    bot = telebot.TeleBot(tok)

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('топ автор', 'топ статья', 'подписка')
    password_button = []
    otvet = telebot.types.InlineKeyboardMarkup(row_width=2)
    for item in range(0, len(action)):
        password_button.append(telebot.types.InlineKeyboardButton(f"{action[item]}", callback_data=action[item]))
    password_button1 = telebot.types.InlineKeyboardButton(" ", callback_data='good')
    password_button2 = telebot.types.InlineKeyboardButton(" ", callback_data='bad')
    for item in range(0, len(action)):
        otvet.add(password_button[item])

    @bot.message_handler(commands=["start"])
    def start_message(message):
        print(message.chat.id)
        bot.send_message(message.chat.id, f"Привет!!! {message.from_user.first_name}", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            if call.message:
                if call.data == 'Да':
                    bot.send_message(call.message.chat.id, 'Ёпта! Да не вопрос, шли e-mail в формате @ваш_email')
                if call.data == 'Нет':
                    bot.send_message(call.message.chat.id, 'Не очень то мы и огорчились!')
        except Exception as e:
            print(repr(e))

    @bot.message_handler(content_types=["text"])
    def commands(message):
        if message.text.lower() == "топ автор":
            msg = GeekHubUser.objects.all()
            top = msg[0]
            for item in msg:
                if GeekHubUser.get_total_user_rating(top) < GeekHubUser.get_total_user_rating(item):
                    top = item
            bot.send_message(message.chat.id, f"Никнейм = {top}, Рейтинг = {GeekHubUser.get_total_user_rating(top)}")

        if message.text.lower() == "топ статья":
            msg = Article.sort_articles_by(Article.objects.all(), sort_by='rating')[:1]
            title = Article.objects.filter(title=msg[0])
            urls = Article.objects.filter(title=msg[0]).values('id')
            bot.send_message(message.chat.id, f"{title[0]}\nhttp://127.0.0.1:8000/article/{urls[0]['id']}/")

        if message.text.lower() == "подписка":
            registered_users = TelegramUsers.objects.filter(users_id=message.chat.id)
            if not registered_users:
                msg = TelegramUsers(users_id=message.chat.id)
                msg.save()
                try:
                    bot.send_message(message.chat.id, "Вы успешно подписаны на наши новости."
                                                      "Хотите привязать аккаунт Телеграма к аккаунту на сайте?",
                                     reply_markup=otvet)
                except Exception as ex:
                    print(ex)
            else:
                try:
                    bot.send_message(message.chat.id, "Ёпта! Да Вы уже подписаны на наши новости!!!"
                                                      "Хотите привязать аккаунт Телеграма к аккаунту на сайте?",
                                     reply_markup=otvet)
                except Exception as ex:
                    print(ex)

        if message.text.lower()[:1] == "@":
            check_email = parseaddr(message.text.lower()[1:])
            if check_email[1] != '':
                verify_link = f"/telegram/{message.chat.id}:{check_email[1]}/"

                title = f'Подтверждение учетной записи {message.chat.id}'
                email_message = f'Для подтверждения учетной записи {message.chat.id} на портале {settings.DOMAIN_NAME} перейдите по ' \
                                f'ссылке: \n{settings.DOMAIN_NAME}{verify_link} '
                send_mail(title, email_message, settings.EMAIL_HOST_USER, [check_email[1]], fail_silently=False,
                          auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD)
                bot.send_message(message.chat.id, f"{email_message}")

    bot.infinity_polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_bot(token)
