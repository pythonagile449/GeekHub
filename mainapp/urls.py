from django.urls import path, include

from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.Index.as_view(), name='index'),
    path('hub/<int:hub_id>/', mainapp.ArticlesByHub.as_view(), name='hubs'),
    path('create-article/', mainapp.CreateArticle.as_view(), name='create_article'),
    path('create-draft/', mainapp.CreateArticle.as_view(), name='create_draft'),
    path('article/<uuid:pk>/rating/', include('ratingsapp.urls', namespace='ratingsapp')),
    path('edit-draft/<uuid:pk>/', mainapp.ArticleUpdate.as_view(), name='edit_draft'),
    path('publish/<uuid:pk>/', mainapp.ArticleUpdate.as_view(), name='article_publication'),
    path('moderation/<uuid:pk>/', mainapp.ArticleUpdate.as_view(), name='article_moderation'),
    path('moderation-list/', mainapp.ModerationList.as_view(), name='moderation_list'),
    path('send_article_on_moderation/<uuid:pk>/', mainapp.ArticleUpdate.as_view(), name='send_article_on_moderation'),
    path('article/<uuid:pk>/', mainapp.ArticleDetail.as_view(), name='article_detail'),
    path('drafts/', mainapp.UserDrafts.as_view(), name='drafts'),
    path('user-articles/', mainapp.UserArticles.as_view(), name='user_articles'),
    path('user-wait-moderation-articles/', mainapp.UserModeratingArticles.as_view(), name='user_moderation_articles'),
    path('user-article-delete/<uuid:pk>/', mainapp.ArticleDelete.as_view(), name='user_article_delete'),
    path('user-article-return-to-drafts/<uuid:pk>/', mainapp.ArticleReturnToDrafts.as_view(),
         name='user_article_to_drafts'),
    path('user/<uuid:pk>/', mainapp.user_detail, name='user_detail'),
    path('get-top-menu/<str:hub_name>', mainapp.top_menu, name='top_menu'),
]
