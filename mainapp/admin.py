from django.contrib import admin
from django.db import models
from martor.admin import MartorModelAdmin
from martor.widgets import AdminMartorWidget

from mainapp.models import Hub, Article

admin.site.register(Hub)


class ArticleAdmin(MartorModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    class Media:
        js = ('plugins/js/jquery.min.js', 'plugins/js/bootstrap.min.js',)
        css = {
            'all': ('plugins/css/bootstrap.min.css',),
        }


admin.site.register(Article, ArticleAdmin)
