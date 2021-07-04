from django.urls import path, include
from commentsapp import views as comment

app_name = 'commentsapp'

urlpatterns = [
    path('create-comment/', comment.create_comment, name='create_comment'),
]
