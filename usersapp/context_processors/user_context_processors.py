from mainapp.models import Article


def usersapp_context(request):
    user = request.user
    user_drafts_count = Article.objects.filter(author=user, is_draft=True, is_deleted=False).count()
    user_published_articles_count = Article.objects.filter(author=user, is_published=True, is_deleted=False).count()
    return {
        'user_drafts_count': user_drafts_count,
        'user_published_articles_count': user_published_articles_count
    }
