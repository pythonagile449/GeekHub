from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from usersapp.models import GeekHubUser


class Complaint(models.Model):
    sender = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE, verbose_name='Отправитель',
                               related_name='complaint_sender', null=True)
    message = models.CharField(max_length=512, verbose_name='Жалоба', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    object_id = models.CharField(max_length=40, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return f'{self.sender} -> {self.content_object.name} -> {self.message[:15]}'
