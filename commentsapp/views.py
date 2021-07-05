import json

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
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


def get_article_comments(request, article_id=None):
    if request.method == 'GET' and request.is_ajax():
        #     get comments logic
        article = get_object_or_404(Article, id=article_id)
        print(article)
        comments = CommentsBranch.objects.filter(article=article)
        print(comments)
        return render(request, 'commentsapp/comments-tree.html', {'comments': comments})
    else:
        return JsonResponse('not ajax GET', safe=False)
