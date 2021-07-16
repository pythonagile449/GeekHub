from django import template

from commentsapp.models import CommentsBranch

register = template.Library()


def get_comments_count(pk):
    return CommentsBranch.get_comments_count_by_article(pk)


register.filter('get_comments_count', get_comments_count)
