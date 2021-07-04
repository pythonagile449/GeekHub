from django.urls import path, include
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.Index.as_view(), name='index'),
    path('hub/<int:hub_id>/', mainapp.ArticlesByHub.as_view(), name='hubs'),
    path('create-article/', mainapp.CreateArticle.as_view(), name='create_article'),
    path('create-draft/', mainapp.CreateArticle.as_view(), name='create_draft'),
    path('article/<uuid:pk>/rating/', include('ratingsapp.urls', namespace='ratingsapp')),
    path('article/<uuid:pk>/', mainapp.ArticleDetail.as_view(), name='article_detail'),

    path('drafts/', mainapp.UserDrafts.as_view(), name='drafts'),
    path('user-articles/', mainapp.UserArticles.as_view(), name='user_articles'),
    path('user-wait-moderation-articles/', mainapp.UserModeratingArticles.as_view(), name='user_moderation_articles'),
    path('user-article-delete/<uuid:pk>/', mainapp.ArticleDelete.as_view(), name='user_article_delete'),
    path('user-article-return-to-drafts/<uuid:pk>/', mainapp.ArticleReturnToDrafts.as_view(),

         name='user_article_to_drafts'),
]
