from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import get_object_or_404

from mainapp.models import Article
from ratingsapp.models import RatingCount
from usersapp.models import GeekHubUser


class Comment(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    rating_id = models.UUIDField(default=uuid4)
    rating = GenericRelation(RatingCount, related_query_name='comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(verbose_name='Текст комментария', blank=True)
    author = models.ForeignKey(GeekHubUser, verbose_name='Автор комментария', on_delete=models.SET_NULL, null=True,
                               blank=True)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    hash_view = models.CharField(max_length=256, blank=True)

    is_moderation = models.BooleanField(default=False)

    def __str__(self):
        if self.parent_comment:
            return f'{self.parent_comment}/{self.pk}'
        else:
            return str(self.pk)

    def save(self, **kwargs):
        some_salt = 'some_salt'
        self.hash_view = make_password(self.hash_view, some_salt)
        super().save(**kwargs)


class CommentsBranch(Comment):
    def __init__(self, *args, **kwargs):
        super(CommentsBranch, self).__init__(*args, **kwargs)

    @staticmethod
    def get_comments_count_by_article(article_id):
        article = get_object_or_404(Article, pk=article_id)
        comments = CommentsBranch.objects.filter(article=article)
        if article.is_published:
            comments_count = comments.filter(is_moderation=False).count()
        else:
            comments_count = comments.filter(is_moderation=True).count()
        return comments_count

    @staticmethod
    def get_last_comments(article_id, comments_count):
        article = get_object_or_404(Article, pk=article_id)
        comments = CommentsBranch.objects.filter(article=article).order_by('-created_at')
        if article.is_published:
            comments = comments.filter(is_moderation=False)
        else:
            comments = comments.filter(is_moderation=True)
        return comments[:comments_count]
