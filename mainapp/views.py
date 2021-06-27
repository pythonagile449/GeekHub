from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from mainapp.forms import ArticleForm
from mainapp.models import Hub, Article


def mainpage(request):
    context = {
        'hubs': Hub.objects.all(),
        'articles': Article.objects.all()
    }

    return render(request, 'mainapp/index.html', context)


def hubs(request, hub_name):
    filtered_articles = Article.objects.filter(hub=hub_name)

    context = {
        'hub_name': hub_name,
        'hubs': Hub.objects.all(),
        'articles': filtered_articles
    }

    return render(request, 'mainapp/hub.html', context)


class CreateArticle(CreateView):
    """
    Создание статьи
    """
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('mainapp:index')

    def form_valid(self, form):
        """
        Устанавливаем инстанс автора статьи для FK модели Article
        """
        form.instance.author = self.request.user
        return super(CreateArticle, self).form_valid(form)


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'
