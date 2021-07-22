from django.contrib.auth.models import AnonymousUser

from complaintsapp.models import Complaint  # Даня
from mainapp.models import Article


def usersapp_context(request):
    user = request.user
    user_drafts_count = 0
    user_published_articles_count = 0
    user_on_moderation_articles_count = 0
    articles_on_moderation_count = 999  # Мажит
    user_articles = ''  # Мажит
    # articles_on_moderation_count = 0  # Даня
    # complaints_count = 0  # Даня
    if not isinstance(user, AnonymousUser):
        user_articles = Article.objects.filter(author=user)
        user_drafts_count = user_articles.filter(is_draft=True, is_deleted=False).count()
        user_published_articles_count = user_articles.filter(is_published=True, is_deleted=False).count()
        user_on_moderation_articles_count = user_articles.filter(is_moderation_in_progress=True,
                                                                 is_deleted=False).count()
        # complaints_count = Complaint.objects.filter(sender=user).count()  # Даня
        if user.is_staff:
            articles_on_moderation_count = Article.objects.filter(is_moderation_in_progress=True,
                                                                  is_deleted=False).count()
 #           complaints_count = Complaint.objects.filter(status='M').count()  # Даня
    return {
        'user_drafts_count': user_drafts_count,
        'user_published_articles_count': user_published_articles_count,
        'user_on_moderation_articles_count': user_on_moderation_articles_count,
        'articles_on_moderation_count': articles_on_moderation_count,
#        'complaints_count': complaints_count,  # Даня
         'user_articles': user_articles  # Мажит
    }
