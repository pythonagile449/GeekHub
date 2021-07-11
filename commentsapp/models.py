from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.hashers import make_password

from ratingsapp.models import RatingCount
from usersapp.models import GeekHubUser
from mainapp.models import Article


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
        return CommentsBranch.objects.filter(article_id=article_id).count()

    @staticmethod
    def get_last_comments(article_id, comments_count):
        return CommentsBranch.objects.filter(article_id=article_id).order_by('-created_at')[:comments_count]
