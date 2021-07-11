from django import template

from notifyapp.models import Notification

register = template.Library()


def get_notifications_count(pk):
    return Notification.objects.filter(recipient=pk, is_read=False).count()


register.filter('notifications_count', get_notifications_count)
