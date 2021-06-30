from django.db import models
from django.contrib.auth.hashers import make_password
from usersapp.models import GeekHubUser
from mainapp.models import Article


# Create your models here.


class Comment(models.Model):
    class Meta:
        abstract = True

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
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


class LikeArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    users = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE)


class LikeComments(models.Model):
    comment = models.ForeignKey(CommentsBranch, on_delete=models.CASCADE)
    users = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE)
