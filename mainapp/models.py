from uuid import uuid4

from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from martor.models import MartorField
from ckeditor_uploader.fields import RichTextUploadingField
from bs4 import BeautifulSoup
from usersapp.models import GeekHubUser
from ratingsapp.models import RatingCount


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
    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=256)
    front_image = models.ImageField(upload_to='article_front_img', blank=True)
    contents_ck = RichTextField(blank=True)
    contents_md = MartorField(blank=True)
    editor = models.CharField(max_length=2, verbose_name='Редактор статьи')
    short_description = models.CharField(max_length=256, blank=True)
    publication_date = models.DateTimeField(auto_now=True, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True, null=False)

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

    def __str__(self):
        return f'{self.title} {self.hub.name}'

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
