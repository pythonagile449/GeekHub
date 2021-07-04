import json

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from commentsapp.models import Comment, CommentsBranch
from mainapp.models import Article


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
        return HttpResponse(
            json.dumps({
                "comment": comment_text,
            }),
            content_type="application/json"
        )
    else:
        return JsonResponse('not ajax GET', safe=False)
