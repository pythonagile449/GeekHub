from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DeleteView

from notifyapp.models import Notification


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
        print(request.POST)
        return super(DeleteNotifications, self).post(request)


def check_notifications(request):
    user_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'notifications_count': user_notifications_count})
