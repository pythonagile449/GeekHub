from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    # path('', mainapp.mainpage, name='index'),
    path('', mainapp.Index.as_view(), name='index'),
    # path('hub/<str:hub_name>', mainapp.hubs, name='hubs'),
    path('hub/<int:hub_id>/', mainapp.ArticlesByHub.as_view(), name='hubs'),
    path('create-article/', mainapp.CreateArticle.as_view(), name='create_article'),
    path('article/<uuid:pk>/', mainapp.ArticleDetail.as_view(), name='article_detail'),
]
