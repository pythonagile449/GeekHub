from django import template
from django.db.models import Sum

from ratingsapp.models import RatingCount

register = template.Library()


def get_positive(pk):
    return RatingCount.objects.filter(object_id=pk, rate__gt=0).count()


def get_negative(pk):
    return RatingCount.objects.filter(object_id=pk, rate__lt=0).count()


def get_total(pk):
    return RatingCount.objects.filter(object_id=pk).aggregate(Sum('rate')).get('rate__sum') or 0


register.filter('rating_positive', get_positive)
register.filter('rating_negative', get_negative)
register.filter('rating_total', get_total)
