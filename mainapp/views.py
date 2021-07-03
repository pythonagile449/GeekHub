import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from mainapp.forms import ArticleCkForm, ArticleMdForm
from mainapp.models import Hub, Article


class Index(ListView):
    """ Главная страница (все статьи). """
    template_name = 'mainapp/index.html'
    queryset = Article.objects.filter(is_published=True).order_by('-publication_date')
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
        queryset = Article.objects.filter(hub=self.kwargs['hub_id'], is_published=True, is_deleted=False) \
            .oreder_by('-publication_date')
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
    success_url = reverse_lazy('mainapp:user_articles')

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
        Set author of article instance for FK Article.
        Create draft if '/create-draft/' or send article on moderation.
        """
        form.instance.author = self.request.user

        # TODO временно статьи создаются в статусе опубликовано, необходимо изменить на модерацию
        # если запрос на публикацию статьи - устанавливаем статус 'на модерации', снимаем статус 'черновик'
        if self.request.path == '/create-article/':
            # form.instance.is_moderation_in_progress = True
            form.instance.is_published = True
            form.instance.is_draft = False
        if self.request.path == '/create-draft/':
            self.success_url = reverse_lazy('mainapp:drafts')
        form_content = self.request.POST['contents']

        # set editor to articles model form
        if form.instance.author.article_redactor == 'CK':
            form.instance.contents_ck = form_content
            form.instance.editor = 'CK'
        if form.instance.author.article_redactor == 'MD':
            form.instance.contents_md = form_content
            form.instance.editor = 'MD'

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


class ArticleUpdate(UpdateView):
    model = Article
    fields = ['title', 'hub']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data()
        context['title'] = f'Редактирование статьи {self.object.title[:10]}'
        # TODO написать контекстные процессоры для количества статей и хабов
        context['hubs'] = Hub.objects.all()
        context['user_drafts_count'] = Article.objects.filter(author=self.object.author, is_draft=True).count()
        context['user_articles_published_count'] = Article.objects.filter(author=self.object.author,
                                                                          is_published=True).count()
        return context

    def get_initial(self):
        initial = super(ArticleUpdate, self).get_initial()
        if self.object.editor == 'CK':
            initial['contents'] = self.object.contents_ck
        if self.object.editor == 'MD':
            initial['contents'] = self.object.contents_md
        return initial

    def get_form_class(self):
        """ Set an editor (self.form_class) depending on article editor. """
        if self.object.editor == 'CK':
            self.form_class = ArticleCkForm
        if self.object.editor == 'MD':
            self.form_class = ArticleMdForm
        return self.form_class


class UserArticles(ListView):
    """ Cтатьи пользователя. По умолчанию отображает "мои статьи". """
    template_name = 'mainapp/user_articles_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_published=True, is_deleted=False) \
            .order_by('-publication_date')
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
        queryset = Article.objects.filter(author=self.request.user, is_draft=True, is_deleted=False) \
            .order_by('-publication_date')
        return queryset


class UserModeratingArticles(UserArticles):
    """ Статьи пользователя на модерации. """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_moderation_in_progress=True, is_deleted=False) \
            .order_by('-publication_date')
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
