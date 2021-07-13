from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import AbstractUser


class GeekHubUser(AbstractUser):
    other = 'O'
    male = 'M'
    female = 'W'

    GENDER_CHOISES = (
        (other, 'другой'),
        (male, 'мужской'),
        (female, 'женский'),
    )

    activate_key = models.CharField(verbose_name='Код активации', max_length=128, blank=True, null=True)
    activate_key_expires = models.DateTimeField(verbose_name='Время действия кода активации',
                                                default=(now() + timedelta(hours=1)))
    email = models.EmailField(verbose_name='E-mail', unique=True)
    profile_photo = models.ImageField(upload_to='media', verbose_name='Фотография профиля', blank=True)
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    user_information = models.CharField(blank=True, max_length=512, verbose_name='Обо мне', default='')
    gender = models.CharField(max_length=1, choices=GENDER_CHOISES, verbose_name='Пол', default=other)

    md_editor = 'MD'
    ckeditor = 'CK'

    REDACTOR_CHOISES = (
        (md_editor, 'markdown'),
        (ckeditor, 'сkeditor'),
    )
    article_redactor = models.CharField(max_length=2, choices=REDACTOR_CHOISES, verbose_name='Редактор статей',
                                        default=ckeditor)

    def is_activate_key_expired(self):
        if now() <= self.activate_key_expires:
            # ToDo: тут логируем что активация невозможна из-за устаревания активационного кода
            return False
        return True

    def get_absolute_url(self):
        return reverse('usersapp:login')


class BlockingByIp(models.Model):
    class Meta:
        db_table = "BlockingByIp"
        verbose_name = "Блокировку по IP"
        verbose_name_plural = "Блокировки по IP"

    ip_address = models.GenericIPAddressField("IP адрес")
    failed_attempts = models.IntegerField("Неудачных попыток", default=0)
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)
    blocking_status = models.BooleanField("Статус блокировки", default=False)

    def __str__(self):
        return self.ip_address


class BlockingByIpAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocking_status', 'failed_attempts', 'time_unblock')
    search_fields = ('ip_address',)
