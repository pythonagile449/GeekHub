import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DeleteView

from notifyapp.models import Notification


# todo docstings for views
class UsersNotificationsList(ListView):
    model = Notification
    template_name = 'user_notifications.html'
    context_object_name = 'notifications'

    def get(self, request, *args, **kwargs):
        users_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        for notification in users_notifications:
            notification.is_read = True
            notification.save()
        return super(UsersNotificationsList, self).get(request, args, kwargs)

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
        return queryset


class DeleteNotifications(View):
    model = Notification

    def post(self, request):
        if request.is_ajax() and request.POST.get('ids'):
            decoded_ids = json.loads(request.POST['ids'])
            notifications_ids = [int(id) for id in decoded_ids]
            Notification.objects.filter(id__in=notifications_ids).delete()
            return JsonResponse({'deleted_notifications_id': request.POST['ids']})


def check_notifications(request):
    user_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'notifications_count': user_notifications_count})
