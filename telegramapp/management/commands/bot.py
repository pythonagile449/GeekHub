# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from django.core.management import BaseCommand
import telebot
from email.utils import parseaddr

from intergalactic import settings
from mainapp.models import Article
from usersapp.models import GeekHubUser
from telegramapp.models import TelegramUsers
from django.core.mail import send_mail

action = ['Да', 'Нет']
author_action = ['Лидер', 'Топ 5']


def main_bot(tok):
    bot = telebot.TeleBot(tok)

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('топ авторы', 'топ статья', 'подписка')
    password_button, author_button = [], []
    otvet = telebot.types.InlineKeyboardMarkup(row_width=2)
    author_otvet = telebot.types.InlineKeyboardMarkup(row_width=2)
    for item in range(0, len(action)):
        password_button.append(telebot.types.InlineKeyboardButton(f"{action[item]}", callback_data=action[item]))
    for item in range(0, len(author_action)):
        author_button.append(
            telebot.types.InlineKeyboardButton(f"{author_action[item]}", callback_data=author_action[item]))
    password_button1 = telebot.types.InlineKeyboardButton(" ", callback_data='good')
    password_button2 = telebot.types.InlineKeyboardButton(" ", callback_data='bad')
    for item in range(0, len(action)):
        otvet.add(password_button[item])
    for item in range(0, len(author_action)):
        author_otvet.add(author_button[item])

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
                if call.data == 'Лидер':
                    msg = GeekHubUser.objects.all()
                    top = msg[0]
                    for item in msg:
                        if GeekHubUser.get_total_user_rating(top) < GeekHubUser.get_total_user_rating(item):
                            top = item
                    message_to_user = f'Никнейм = <a href="https://reqsoft.ru/auth/user/{top.pk}/">{top}</a>, ' \
                                      f'Рейтинг = {GeekHubUser.get_total_user_rating(top)}'
                    bot.send_message(call.message.chat.id, message_to_user, parse_mode='HTML')
                if call.data == 'Топ 5':
                    msg = GeekHubUser.objects.all()
                    author_list = list()
                    for item in msg:
                        rating = GeekHubUser.get_total_user_rating(item)
                        author_list.append([rating, [str(item), str(item.pk)]])
                    author_list.sort(key=lambda x: x[0])
                    author_list.reverse()
                    
                    message_list = 'Топ 5 авторов:\n'
                    for item in range(0, 5):
                        message_list += f'Никнейм = <a href="https://reqsoft.ru/auth/user/{author_list[item][1][1]}/">' \
                                           f'{author_list[item][1][0]}</a>, ' \
                                           f'Рейтинг = {author_list[item][0]}\n'
                    bot.send_message(call.message.chat.id, message_list, parse_mode='HTML')

        except Exception as e:
            print(repr(e))

    @bot.message_handler(content_types=["text"])
    def commands(message):
        if message.text.lower() == "топ авторы":
            msg = GeekHubUser.objects.all()
            top = msg[0]
            for item in msg:
                if GeekHubUser.get_total_user_rating(top) < GeekHubUser.get_total_user_rating(item):
                    top = item
            bot.send_message(message.chat.id, 'Выберите вариант: ', reply_markup=author_otvet)

        if message.text.lower() == "топ статья":
            msg = Article.sort_articles_by(Article.objects.all(), sort_by='rating')[:1]
            title = Article.objects.filter(title=msg[0])
            urls = Article.objects.filter(title=msg[0]).values('id')
            complite_url = f"https://reqsoft.ru/article/{urls[0]['id']}/"
            bot.send_message(message.chat.id, f'<a href="{complite_url}">{title[0]}</a>', parse_mode='HTML')

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
                email_message = f'Для подтверждения учетной записи {message.chat.id} на портале https://reqsoft.ru перейдите по ' \
                                f'ссылке: \nhttps://reqsoft.ru{verify_link} '
                bot_message = f'Для подтверждения учетной записи {message.chat.id} на портале https://reqsoft.ru перейдите по ' \
                              f'ссылке отправленной вам на email '
                send_mail(title, email_message, settings.EMAIL_HOST_USER, [check_email[1]], fail_silently=False,
                          auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD)
                bot.send_message(message.chat.id, f"{bot_message}")

    bot.infinity_polling()


class Command(BaseCommand):
    help = 'Запускет бота'

    def handle(self, *args, **options):
        main_bot(settings.token)
