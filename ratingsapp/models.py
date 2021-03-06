from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from usersapp.models import GeekHubUser


class RatingManager(models.Manager):
    """
    RU
        Класс менеджер рейтингов.
        Методы класса:
        positive: Получаем queryset с записями больше 0
        negative: Получаем queryset с записями меньше 0
        total: Получаем суммарный рейтинг

    EN
        Rating manager class
        Class methods:
        positive: get queryset with positive entries
        negative: get queryset with negative entries
        total: get rating summary
    """
    use_for_related_fields = True

    def positive(self):
        return self.get_queryset().filter(rate__gt=0)

    def negative(self):
        return self.get_queryset().filter(rate__lt=0)

    def total(self):
        return self.get_queryset().aggregate(Sum('rate')).get('rate__sum') or 0


class RatingCount(models.Model):
    class Meta:
        verbose_name = "Счетчик рейтинга"
        verbose_name_plural = "Счетчики рейтинга"

    POSITIVE = 1
    NEGATIVE = -1

    OPTION = (
        (POSITIVE, 'LIKE'),
        (NEGATIVE, 'DISLIKE'),
    )

    rate = models.IntegerField(verbose_name='Рейтинг', choices=OPTION)
    users = models.ForeignKey(GeekHubUser, verbose_name='Владелец', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=40)
    content = GenericForeignKey()
    objects = RatingManager()

    @staticmethod
    def get_user_rate_chose(user, obj_id, obj_content_type):
        try:
            rate = RatingCount.objects.get(content_type=obj_content_type, object_id=obj_id, users=user).rate
        except RatingCount.DoesNotExist:
            rate = 0
        except TypeError:
            rate = 0
        return rate
