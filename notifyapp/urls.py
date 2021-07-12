from django.urls import path, include
from notifyapp import views as notifyapp

app_name = 'notifyapp'

urlpatterns = [
    path('', notifyapp.UsersNotificationsList.as_view(), name='user_notifications'),
    path('check-user-notifications-count/', notifyapp.check_notifications, name='get_notification_count'),
    path('delete-notifications/', notifyapp.DeleteNotifications.as_view(), name='delete_notifications'),
]
