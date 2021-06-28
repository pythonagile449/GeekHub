from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from mainapp.forms import ArticleCkForm, ArticleMdForm
from mainapp.models import Hub, Article


class Index(ListView):
    """ Главная страница (все статьи). """
    template_name = 'mainapp/index.html'
    queryset = Article.objects.filter(is_published=True)
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
        queryset = Article.objects.filter(hub=self.kwargs['hub_id'], is_published=True)
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
    success_url = reverse_lazy('mainapp:index')

    def get_form_class(self):
        """ Установка редактора (self.form_class) в зависимости от настроек пользователя. """
        user = self.request.user
        if user.article_redactor == 'CK':
            self.form_class = ArticleCkForm
        if user.article_redactor == 'MD':
            self.form_class = ArticleMdForm
        return self.form_class

    def form_valid(self, form):
        """
        Устанавливает инстанс автора статьи для FK модели Article.
        Создает черновик есть action формы '/create-draft/'.
        """
        form.instance.author = self.request.user

        # если запрос на публикацию статьи - устанавливаем статус 'на модерации', снимаем статус 'черновик'
        if self.request.path != '/create-draft/':
            form.instance.is_moderation_in_progress = True
            form.instance.is_draft = False

        # добавляем посфикс для определения редактора в шаблоне вида '<CK>' или '<MD>'
        form.instance.contents += f'<{form.instance.author.article_redactor}>'
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


class UserArticles(ListView):
    """ Cтатьи пользователя. По умолчанию отображает "мои статьи". """
    template_name = 'mainapp/user_articles_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_published=True)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hubs'] = Hub.objects.all()
        context['title'] = 'Мои статьи'
        return context


class UserDrafts(UserArticles):
    """ Черновики пользователя. """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_draft=True)
        return queryset


class UserModeratingArticles(UserArticles):
    """ Статьи пользователя на модерации. """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_moderation_in_progress=True)
        return queryset
