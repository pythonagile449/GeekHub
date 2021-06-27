from uuid import uuid4
from django.db import models
from martor.models import MartorField
from usersapp.models import GeekHubUser


class Hub(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Хаб'
        verbose_name_plural = 'Хабы'

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=256)
    front_image = models.ImageField(upload_to='article_front_img', blank=True)
    # contents = models.TextField(blank=True)
    contents = MartorField()
    short_description = models.CharField(max_length=256, blank=True)
    publication_date = models.DateField(auto_now=True, blank=False, null=False)

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    author = models.ForeignKey(GeekHubUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.title} {self.hub.name}'

    def get_first_paragraph(self):
        """
        Возвращает первый абзац статьи для отображения в списке статей (на главной и по хабам).
        """
        return self.contents.split('\n')[0]
