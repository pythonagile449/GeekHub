# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from usersapp.models import GeekHubUser
from django.shortcuts import render


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

