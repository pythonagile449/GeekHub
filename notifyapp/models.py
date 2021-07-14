from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from usersapp.models import GeekHubUser


class Notification(models.Model):
    sender = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE, verbose_name='Отправитель', related_name='sender')
    recipient = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE, verbose_name='Получатель',
                                  related_name='recipient', null=True)
    message = models.CharField(max_length=512, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    object_id = models.CharField(max_length=40, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.sender} -> {self.recipient}: {self.message[:50]}...'
