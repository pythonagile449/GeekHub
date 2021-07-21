from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from usersapp.models import GeekHubUser


class Notification(models.Model):
    sender = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE, verbose_name='Отправитель', related_name='sender',
                               null=True)
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


class NotificationFactory:
    @classmethod
    def notify(cls, sender, recipient, message, model_object):
        """ Create and return notification object. """
        return Notification.objects.create(
            sender=sender,
            recipient=recipient,
            message=message,
            content_type=ContentType.objects.get_for_model(model_object),
            object_id=model_object.pk,
            content_object=model_object,
        )
