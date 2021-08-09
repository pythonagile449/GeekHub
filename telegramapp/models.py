from django.db import models


# Create your models here.

class TelegramUsers(models.Model):
    users_id = models.CharField(verbose_name='ID', max_length=20, blank=True)
