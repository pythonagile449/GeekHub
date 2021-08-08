from uuid import uuid4

from rhvoice_wrapper import TTS
from threading import Thread

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

    sound = models.ImageField(upload_to='media', verbose_name='Озвученная статья', blank=True)

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
    def get_top_articles(hub_name='Все хабы', count=7, sort_by='rating'):
        """ Return articles by rating. """
        if hub_name == 'Все хабы':
            articles = Article.objects.filter(is_published=True)
        else:
            articles = Article.objects.filter(is_published=True, hub__name=hub_name)
        return Article.sort_articles_by(articles, sort_by)[:count]

    @staticmethod
    def sort_articles_by(articles_queryset, sort_by):
        top_articles = articles_queryset
        if sort_by == 'rating':
            top_articles = sorted([article for article in articles_queryset], key=lambda a: a.rating.total(),
                                  reverse=True)
        if sort_by == 'views':
            views = articles_queryset.prefetch_related('article_view')
            top_articles = sorted([view for view in views],
                                  key=lambda a: ArticleViews.get_views_count_by_article(a.pk), reverse=True)
        if sort_by == 'date':
            top_articles = articles_queryset.order_by('-publication_date')
        return top_articles

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

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_view')
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




class ArticleToSoundThread():

    """https://freesoft.dev/program/148898794"""

    def get_sound_data(self):
        article = self

        sound_path_article = str(article.id)+'.mp3'
        article.sound = sound_path_article
        article.save()
        th = Thread(target=ArticleToSoundThread.get_voice_from_text, args=(self,))
        th.start()
        th.join()
        # ArticleToSoundThread.get_voice_from_text(article)

        return sound_path_article



    def get_voice_from_text(article):
        try:
            article = article
            text = ArticleToSoundThread.get_article_text(article)
            sound_path_article_to_file = 'media' + str(article.sound.url)
            tts = TTS(threads=1)
            tts.to_file(filename=sound_path_article_to_file, text=text, voice='anna', format_='mp3')
            return
        except KeyError:
            return "Error record voice"


    def get_article_text(article):
        """
            Returns the text of the article to be displayed in the article list.
            """
        if article.editor == 'CK':
            return ArticleToSoundThread.get_text_from_content(article.contents_ck)
        if article.editor == 'MD':
            return ArticleToSoundThread.get_text_from_content(article.contents_md)


    def get_text_from_content(html):
        """  Remove all style attrs from tags in ckeditor field"""
        soup = BeautifulSoup(html, features='lxml')
        try:
            text = soup.text
            return text
        except KeyError:
            return html