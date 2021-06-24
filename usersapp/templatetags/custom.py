from django import template
from django.conf import settings

register = template.Library()


def media_folder(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам
    avatar.jpg --> /media/avatar.jpg
    """
    if not string:
        string = 'default.jpg'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder', media_folder)
