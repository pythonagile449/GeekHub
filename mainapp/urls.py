from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.mainpage, name='index'),
    path('hub/<str:hub_name>', mainapp.hubs, name='hubs'),
    path('create-article/', mainapp.CreateArticle.as_view(), name='create_article'),
]


