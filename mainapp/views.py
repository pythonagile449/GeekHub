from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from mainapp.forms import ArticleForm
from mainapp.models import Hub, Article


class Index(ListView):
    """ Главная страница (все статьи). """
    template_name = 'mainapp/index.html'
    queryset = Article.objects.all()
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hubs'] = Hub.objects.all()
        context['title'] = 'Главная'
        return context


class ArticlesByHub(ListView):
    """
    Статьи по категориям.
    hub_id передается в kwargs из get_absolute_url модели.
    """
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = Article.objects.filter(hub=self.kwargs['hub_id'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesByHub, self).get_context_data()
        context['title'] = Hub.objects.get(pk=self.kwargs['hub_id'])
        context['hubs'] = Hub.objects.all()
        context['active_hub'] = context['title']
        return context


class CreateArticle(CreateView):
    """ Создание статьи. """
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('mainapp:index')

    def form_valid(self, form):
        """ Устанавливает инстанс автора статьи для FK модели Article."""
        form.instance.author = self.request.user
        return super(CreateArticle, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateArticle, self).get_context_data()
        context['hubs'] = Hub.objects.all()
        context['title'] = 'Создание новой статьи'
        return context


class ArticleDetail(DetailView):
    """ Просмотр статьи."""
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data()
        context['title'] = self.get_object().title
        context['hubs'] = Hub.objects.all()
        return context
