import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from commentsapp.models import CommentsBranch
from mainapp.models import Article
from notifyapp.models import Notification


def create_comment(request):
    if request.method == 'POST' and request.is_ajax():
        form_data = request.POST
        article = Article.objects.get(id=form_data['article_id'])
        comment_text = form_data['comment']
        new_comment = CommentsBranch.objects.create(
            article=article,
            description=comment_text,
            author=request.user,
        )
        if form_data.get('parent_comment_id'):
            new_comment.parent_comment = CommentsBranch.objects.get(id=form_data['parent_comment_id'])
            new_comment.save()

        if request.user != article.author:
            notification = Notification.objects.create(
                sender=request.user,
                recipient=article.author,
                message='Новый комментарий к статье',
                content_type=ContentType.objects.get_for_model(article),
                object_id=article.pk,
                content_object=article,
            )

        return HttpResponse(
            json.dumps({
                'comments_count': CommentsBranch.get_comments_count_by_article(article.pk),
            }),
            content_type="application/json",
        )
    else:
        return HttpResponse(status=404)


def get_article_comments(request, article_id=None):
    if request.method == 'GET' and request.is_ajax():
        article = get_object_or_404(Article, id=article_id)
        comments = CommentsBranch.objects.filter(article=article).order_by('-created_at')
        return render(request, 'commentsapp/comments-tree.html', {'comments': comments, 'article': article})
    else:
        return HttpResponse(status=404)
