from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import datetime
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from commentsapp.models import CommentsBranch
from mainapp.forms import ArticleCkForm, ArticleMdForm
from mainapp.models import Hub, Article, ArticleViews
from notifyapp.models import Notification
from ratingsapp.models import RatingCount
from usersapp.views import get_user_ip


class Index(ListView):
    """
    RU
    Главная страница (все статьи).

    EN
    Main paige(all the articles by publication date)
    """
    model = Article
    template_name = 'mainapp/index.html'
    queryset = Article.objects.filter(is_published=True)
    ordering = ['-publication_date']
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class ArticlesByHub(Index):
    """
    RU
    Статьи по категориям.
    hub_id передается в kwargs из get_absolute_url модели.

    EN
    Articles by categories(hubs)
    hub_id is passed in kwargs from the get_absolute_url model method
    """

    def get_queryset(self):
        queryset = Article.objects.filter(hub=self.kwargs['hub_id'], is_published=True, is_deleted=False) \
            .order_by('-publication_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesByHub, self).get_context_data()
        context['title'] = Hub.objects.get(pk=self.kwargs['hub_id'])
        context['active_hub'] = context['title']
        return context


class CreateArticle(CreateView):
    """
    RU
    Создание статьи.

    EN
    Create article
    """
    model = Article
    success_url = reverse_lazy('mainapp:user_moderation_articles')

    def get_form_class(self):
        """
        RU
        Установка редактора (self.form_class) в зависимости от настроек пользователя.

        EN
        Setup the editor (self.form_class) depending on user's preferences
        """
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

        # если запрос на публикацию статьи - устанавливаем статус 'на модерации', снимаем статус 'черновик'
        # if publication of an article is requested, set status 'is_moderation_in_progress' remove status 'draft'
        if self.request.path == '/create-article/':
            form.instance.is_moderation_in_progress = True
            form.instance.is_draft = False
        if self.request.path == '/create-draft/':
            self.success_url = reverse_lazy('mainapp:drafts')
        form.instance.publication_date = datetime.datetime.now()
        form_content = self.request.POST['contents']

        # set editor to articles model form
        if form.instance.author.article_redactor == 'CK':
            form.instance.contents_ck = Article.remove_style_tag_from_ck_content(form_content)
            form.instance.editor = 'CK'
        if form.instance.author.article_redactor == 'MD':
            form.instance.contents_md = form_content
            form.instance.editor = 'MD'

        return super(CreateArticle, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateArticle, self).get_context_data()
        context['title'] = 'Создание новой статьи'
        return context


class ArticleDetail(DetailView):
    """
    RU
    Просмотр статьи.

    EN
    Article viewing
    """
    model = Article
    context_object_name = 'article'
    comments_preview_count = 3

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data()
        context['title'] = self.get_object().title
        context['comments_preview'] = CommentsBranch.get_last_comments(self.get_object().pk,
                                                                       self.comments_preview_count)
        context['comments_count_settings'] = self.comments_preview_count
        context['all_comments_count'] = CommentsBranch.get_comments_count_by_article(self.get_object().pk)
        context['user_rating_for_article_chose'] = RatingCount.get_user_rate_chose(
            user=self.request.user, obj_id=self.object.id,
            obj_content_type=ContentType.objects.get_for_model(self.object))
        return context

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetail, self).get(request, *args, **kwargs)
        if self.object.is_published:
            user_ip = get_user_ip(request)
            if request.user.is_authenticated:
                ArticleViews.get_or_add_auth_user_view(self.object.pk, request.user.pk, user_ip)
            else:
                ArticleViews.get_or_add_anonymous_view(self.object.pk, user_ip)
        return response


class ArticleUpdate(UpdateView):
    """ Editing an article. """
    model = Article
    fields = ['title', 'hub']

    def get(self, request, *args, **kwargs):
        article = self.get_object()

        if request.path.startswith('/send_article_on_moderation/'):
            # handle send on moderation action under user drafts list
            article.set_on_moderation_status()
            article.publication_date = datetime.datetime.now()
            self.success_url = reverse_lazy('mainapp:drafts')
            article.save()
            return HttpResponseRedirect(self.success_url)
        if request.path.startswith('/publish/'):
            # handle publish action under staff user
            if request.user.is_staff:
                article.set_publish_status()
                article.publication_date = datetime.datetime.now()
                article.save()
                self.success_url = reverse_lazy('mainapp:moderation_list')

                # create new notification to author
                notification = Notification.objects.create(
                    sender=request.user,
                    recipient=article.author,
                    message='Статья опубликована',
                    content_type=ContentType.objects.get_for_model(article),
                    object_id=article.pk,
                    content_object=article,
                )
                return HttpResponseRedirect(self.success_url)
        return super(ArticleUpdate, self).get(request, args, kwargs)

    def form_invalid(self, form):
        """ Processing an incorrect ajax request to change data. """
        if self.request.method == 'POST' and self.request.is_ajax():
            return JsonResponse('Error', safe=False)
        else:
            return super(ArticleUpdate, self).form_invalid(form)

    def set_object_contents(self, form):
        """ Set article model field extends redactor. """
        if self.object.editor == 'CK':
            self.object.contents_ck = Article.remove_style_tag_from_ck_content(form.cleaned_data['contents'])
        if self.object.editor == 'MD':
            self.object.contents_md = form.cleaned_data['contents']

    def form_valid(self, form):
        """ Processing a correct ajax request to change data. """
        if self.request.method == 'POST' and self.request.is_ajax():
            # ajax request mean that there is a 'save draft' action
            self.set_object_contents(form)
            self.object.save()
            return JsonResponse('Success', safe=False)
        elif self.request.method == 'POST' and not self.request.is_ajax():
            self.set_object_contents(form)
            if self.request.path.startswith('/publish/'):
                # todo handle publication action (for high rating users)
                if self.request.user.is_staff:
                    self.object.set_publish_status()
                    self.success_url = reverse_lazy('mainapp:article_detail', self.object.pk)
            elif self.request.path.startswith('/moderation/'):
                # handle moderation action
                self.set_object_contents(form)
                self.object.set_on_moderation_status()
                self.success_url = reverse_lazy('mainapp:user_moderation_articles')
            self.object.publication_date = datetime.datetime.now()
            self.object.save()
            return super(ArticleUpdate, self).form_valid(form)
        else:
            return super(ArticleUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data()
        context['title'] = f'Редактирование статьи {self.object.title[:10]}'
        context['edit_flag'] = True  # set a flag to tell the template to render the "save changes" buttons
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
    """
    RU
    Cтатьи пользователя. По умолчанию отображает "мои статьи".

    EN
    User's articles. By deafault shows "my articles"
    """
    template_name = 'mainapp/user_articles_list_table.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_published=True, is_deleted=False) \
            .order_by('-publication_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_published'] = True
        context['is_draft'] = False
        context['is_on_moderation'] = False
        context['title'] = 'Мои статьи'
        return context


class UserDrafts(UserArticles):
    """
    RU
    Черновики пользователя.

    EN
    User's drafts
    """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_draft=True, is_deleted=False) \
            .order_by('-publication_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDrafts, self).get_context_data(**kwargs)
        context['is_published'] = False
        context['is_draft'] = True
        context['is_on_moderation'] = False
        return context


class UserModeratingArticles(UserArticles):
    """
    RU
    Статьи пользователя на модерации.

    EN
    User's articles being reviewed by moderators
    """

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user, is_moderation_in_progress=True, is_deleted=False) \
            .order_by('-publication_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserModeratingArticles, self).get_context_data(**kwargs)
        context['is_published'] = False
        context['is_draft'] = False
        context['is_on_moderation'] = True
        return context


class ArticleDelete(DeleteView):
    """ Delete article view. """
    model = Article
    template_name = 'mainapp/article_confirm_delete.html'
    success_url = reverse_lazy('mainapp:drafts')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.set_deleted_status()
        return HttpResponseRedirect(self.success_url)


class ArticleReturnToDrafts(DeleteView):
    """ Return article to draft by user or moderator. """
    model = Article
    template_name = 'mainapp/article_confirm_to_drafts.html'
    success_url = reverse_lazy('mainapp:drafts')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_published = self.object.is_published
        self.object.set_draft_status()
        if request.user.is_staff:
            self.object.reason_for_reject = request.POST.get('reason_article_reject')
            self.object.save()
        if request.user != self.object.author:
            Notification.objects.create(
                sender=request.user,
                recipient=self.object.author,
                message=f'Статья снята с {"публикации" if is_published else "модерации"}.',
                content_type=ContentType.objects.get_for_model(self.object),
                object_id=self.object.pk,
                content_object=self.object,
            )
        return HttpResponseRedirect(self.get_success_url())


class ModerationList(ListView):
    """
    RU
    Страница профиля модератора (модерация статей пользователей).

    EN
    Moderators profile page (moderation users articles).
    """
    template_name = 'mainapp/user_articles_list_table.html'
    queryset = Article.objects.filter(is_moderation_in_progress=True, is_deleted=False).order_by('publication_date')
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ModerationList, self).get_context_data()
        context['title'] = 'Модерация статей'
        context['is_published'] = False
        context['is_draft'] = False
        context['is_on_moderation'] = True
        return context


class TopMenuView(View):
    """
    RU
    Контроллер меню топа статей.

    EN
    Top articles' menu controller
    """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            hub_name = self.kwargs.get('hub_name')
            sort_by = request.GET.get('sorted_by')

            return render(request, 'mainapp/top-menu.html',
                          {'top_articles': Article.get_top_articles (hub_name=hub_name,
                                                         sort_by=sort_by if sort_by else 'rating')})
        else:
            return HttpResponse(status=404)
