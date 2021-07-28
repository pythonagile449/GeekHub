from uuid import uuid4

from bs4 import BeautifulSoup
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import Count
from django.urls import reverse
from martor.models import MartorField

from ratingsapp.models import RatingCount
from usersapp.models import GeekHubUser


class Hub(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Хаб'
        verbose_name_plural = 'Хабы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mainapp:hubs', kwargs={'hub_id': self.pk})


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, db_index=True)
    title = models.CharField(max_length=256)
    front_image = models.ImageField(upload_to='article_front_img', blank=True)
    contents_ck = RichTextField(blank=True)
    contents_md = MartorField(blank=True)
    editor = models.CharField(max_length=2, verbose_name='Редактор статьи')
    short_description = models.CharField(max_length=256, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True, null=False)
    views = models.PositiveIntegerField(verbose_name='Просмотры статьи', default=0)
    reason_for_reject = models.CharField(max_length=512, verbose_name='Причина снятия с публикации', null=True,
                                         blank=True)

    is_draft = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    is_moderation_in_progress = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    author = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE)
    rating = GenericRelation(RatingCount, related_query_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        indexes = [GinIndex(fields=['title'])]

    def __unicode__(self):
        return self.title

    def __str__(self):
        return f'{self.title}'

    def set_deleted_status(self):
        self.is_draft = False
        self.is_published = False
        self.is_moderation_in_progress = False
        self.is_deleted = True
        self.save()

    def set_publish_status(self):
        self.reason_for_reject = None
        self.is_draft = False
        self.is_published = True
        self.is_moderation_in_progress = False
        self.save()

    def set_on_moderation_status(self):
        self.is_draft = False
        self.is_published = False
        self.is_moderation_in_progress = True
        self.save()

    def set_draft_status(self):
        self.is_draft = True
        self.is_published = False
        self.is_moderation_in_progress = False
        self.save()

    def get_views_count(self):
        return ArticleViews.objects.filter(article=self).count()

    def get_rating_count(self):
        return self.rating.total()

    @staticmethod
    def get_top_rated_articles(hub_name='Все хабы', count=7):
        """ Return articles by rating. """
        if hub_name == 'Все хабы':
            articles = Article.objects.filter(is_published=True)
        else:
            articles = Article.objects.filter(is_published=True, hub__name=hub_name)
        top_articles = sorted([a for a in articles], key=lambda a: a.rating.total(), reverse=True)
        return top_articles[:count]

    @staticmethod
    def remove_style_tag_from_ck_content(html):
        """ Remove style attrs from image tags in ckeditor field. """
        soup = BeautifulSoup(html, features='lxml')
        images = soup.find_all('img')
        try:
            for image in images:
                image.attrs.pop('style')
            return ''.join([str(tag) for tag in soup.body.children])
        except KeyError:
            return html

    def get_article_preview_from_ck(self):
        """ Uses BeatifulSoup to parse html. """
        soup = BeautifulSoup(self.contents_ck, features='lxml')
        article_tags = soup.find_all('p')
        try:
            first_p, second_p = article_tags[0], article_tags[1]
            if first_p.find_all('img'):
                return str(first_p) + str(second_p)
            return first_p
        except IndexError:
            return article_tags[0]

    def get_article_preview_from_md(self):
        paragraphs = self.contents_md.split('\n')
        clear_paragraphs = []
        for line in paragraphs:
            if line != '\r':
                clear_paragraphs.append(line)
        try:
            first_p, second_p = clear_paragraphs[0], clear_paragraphs[1]
            if first_p.startswith('!['):
                return '\n'.join([first_p, second_p])
            return first_p
        except IndexError:
            return clear_paragraphs[0]

    def get_article_preview(self):
        """
        Returns the first paragraph of the article to be displayed in the article list (on the main page and by hubs).
        If the article begins with a picture, the picture and the first paragraph after the picture are displayed.
        """
        if self.editor == 'CK':
            return self.get_article_preview_from_ck()
        if self.editor == 'MD':
            return self.get_article_preview_from_md()

    def get_absolute_url(self):
        return reverse('mainapp:article_detail', kwargs={'pk': self.pk})


class ArticleViews(models.Model):
    class Meta:
        verbose_name = 'Просмотр статьи'
        verbose_name_plural = 'Просмотры статьи'

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    view_user = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE, null=True, blank=True)
    is_anonymous = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True)
    view_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_views_count_by_article(article_id):
        return ArticleViews.objects.filter(article=article_id).count()

    @staticmethod
    def get_or_add_auth_user_view(article_id, user_id, ip_address):
        return ArticleViews.objects.get_or_create(article_id=article_id, view_user_id=user_id,
                                                  is_anonymous=False, ip_address=ip_address)

    @staticmethod
    def get_or_add_anonimus_view(article_id, ip_address):
        return ArticleViews.objects.get_or_create(article_id=article_id, is_anonymous=True, ip_address=ip_address)
