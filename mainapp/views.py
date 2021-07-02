import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
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
        queryset = Article.objects.filter(hub=self.kwargs['hub_id'], is_published=True, is_deleted=False)
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

        # TODO временно статьи создаются в статусе опубликовано, необходимо изменить на модерацию
        # если запрос на публикацию статьи - устанавливаем статус 'на модерации', снимаем статус 'черновик'
        if self.request.path != '/create-draft/':
            # form.instance.is_moderation_in_progress = True
            form.instance.is_published = True
            form.instance.is_draft = False

        # если используется маркдаун - конвертируем его в html
        if form.instance.author.article_redactor == "MD":
            form.instance.contents = markdown.markdown(form.instance.contents)

        return super(CreateArticle, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateArticle, self).get_context_data()
        context['hubs'] = Hub.objects.all()
        context['title'] = 'Создание новой статьи'
        # TODO написать контекстные процессоры для количества статей
        context['user_drafts_count'] = Article.objects.filter(author=self.request.user, is_draft=True).count()
        context['user_articles_published_count'] = Article.objects.filter(author=self.request.user,
                                                                          is_published=True).count()
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
        queryset = Article.objects.filter(author=self.request.user, is_published=True, is_deleted=False)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hubs'] = Hub.objects.all()
        context['title'] = 'Мои статьи'
        # TODO написать контекстные процессоры для количества статей
        context['user_drafts_count'] = Article.objects.filter(author=self.request.user, is_draft=True).count()
        context['user_articles_published_count'] = Article.objects.filter(author=self.request.user,
                                                                          is_published=True).count()
        return context


class UserDrafts(UserArticles):
    """ Черновики пользователя. """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_draft=True, is_deleted=False)
        return queryset


class UserModeratingArticles(UserArticles):
    """ Статьи пользователя на модерации. """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_moderation_in_progress=True, is_deleted=False)
        return queryset


class ArticleDelete(DeleteView):
    model = Article
    template_name = 'mainapp/article_confirm_delete.html'
    success_url = reverse_lazy('mainapp:drafts')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_published = False
        self.object.is_moderation_in_progress = False
        self.object.is_draft = False
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class ArticleReturnToDrafts(DeleteView):
    model = Article
    template_name = 'mainapp/article_confirm_to_drafts.html'
    success_url = reverse_lazy('mainapp:user_articles')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_published = False
        self.object.is_moderation_in_progress = False
        self.object.is_draft = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
