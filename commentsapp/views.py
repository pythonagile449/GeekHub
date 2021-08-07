import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from commentsapp.models import CommentsBranch
from mainapp.models import Article
from notifyapp.models import NotificationFactory


def create_comment(request):
    if request.method == 'POST' and request.is_ajax():
        form_data = request.POST
        article = Article.objects.get(id=form_data['article_id'])
        comment_text = form_data['comment']
        new_comment = CommentsBranch.objects.create(
            article=article,
            description=comment_text,
            author=request.user,
            is_moderation=True if article.is_draft or article.is_moderation_in_progress else False,
        )
        if form_data.get('parent_comment_id'):
            new_comment.parent_comment = CommentsBranch.objects.get(id=form_data['parent_comment_id'])
            new_comment.save()

        if request.user != article.author:
            message = 'Новое замечание модератора' if not article.is_published else 'Новый комментарий к статье'
            NotificationFactory.notify(sender=request.user,
                                       recipient=article.author,
                                       message=message,
                                       model_object=new_comment)

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
        is_complaint = request.GET.get('complaint_against_comment')
        if article.is_published:
            comments = comments.filter(is_moderation=False)
        else:
            comments = comments.filter(is_moderation=True)

        return render(request, 'commentsapp/comments-tree.html',
                      {'comments': comments, 'article': article,
                       'complaint_against_comment': True if is_complaint == 'True' else False,
                       })
    else:
        return HttpResponse(status=404)
