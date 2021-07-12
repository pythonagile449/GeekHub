from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from ratingsapp.models import RatingCount
from mainapp.models import Article
from commentsapp.models import CommentsBranch

app_name = 'ajax'
urlpatterns = [
    path('article/like/',
         login_required(views.RatingsView.as_view(model=Article, vote_type=RatingCount.POSITIVE)),
         name='article_like'),
    path('article/dislike/',
         login_required(views.RatingsView.as_view(model=Article, vote_type=RatingCount.NEGATIVE)),
         name='article_dislike'),
    path('comment/like/',
         login_required(views.RatingsView.as_view(model=CommentsBranch, vote_type=RatingCount.POSITIVE)),
         name='comment_like'),
    path('comment/dislike/',
         login_required(views.RatingsView.as_view(model=CommentsBranch, vote_type=RatingCount.NEGATIVE)),
         name='comment_dislike'),
]
