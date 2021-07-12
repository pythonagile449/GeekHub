from django import template

from commentsapp.models import CommentsBranch

register = template.Library()


def get_comments_count(pk):
    return CommentsBranch.objects.filter(article_id=pk).count()


register.filter('get_comments_count', get_comments_count)
