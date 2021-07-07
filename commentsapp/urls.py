from django.urls import path, include
from commentsapp import views as comment

app_name = 'commentsapp'

urlpatterns = [
    path('create-comment/', comment.create_comment, name='create_comment'),
    path('get-comments-tree/<uuid:article_id>', comment.get_article_comments, name='get_comments_tree'),
]
