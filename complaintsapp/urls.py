from django.urls import path

from complaintsapp import views as complaint

app_name = 'complaints'

urlpatterns = [
    path('create/', complaint.CreateComplaintView.as_view(), name='create_comment'),
]
