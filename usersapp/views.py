from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView

from mainapp.models import Hub, Article
from usersapp.models import GeekHubUser
from usersapp.forms import RegistrationForm, LoginForm, UserProfileForm, UserProfileEditForm


def main(request):
    """
    Главная страница приложения usersapp
    """
    return render(request, 'usersapp/index.html')


class RegistrationView(CreateView):
    '''
    Представление регистрации пользователя.
    Передаваемый контекст:
    '''
    model = GeekHubUser
    form_class = RegistrationForm
    success_url = '/auth/verify/'


class AuthenticationView(LoginView):
    """
    Аутентификация пользователя
    Контекст: form, содержит поле логина и пароля (пример : {{ form.username }}, или стандартно {{ form.as_p }})
    Имя шаблона: login.html
    """
    form_class = LoginForm
    template_name = 'usersapp/login.html'


class UserLogoutView(LogoutView):
    """
    Выход из аккаунта
    Завершает текущий сеанс работы пользователя, с отображением страницы
    Имя шаблона: logout.html
    """
    template_name = 'usersapp/logout.html'


# class UserAccountView(DetailView):
#     """
#     Профиль пользователя
#     Контекст: object, содержит все поля модели пользователя (пример: {{ object.username }})
#     Имя шаблона: geekhubuser_detail.html
#     """
#     model = GeekHubUser
#     form_class = UserProfileForm
#
#     def get_context_data(self, **kwargs):
#         context = super(UserAccountView, self).get_context_data()
#         context['hubs'] = Hub.objects.all()
#         context['title'] = f'Профиль пользователя {self.object.username}'
#         TODO написать контекстные процессоры для количества статей
# context['user_drafts_count'] = Article.objects.filter(author=self.object, is_draft=True).count()
# context['user_articles_published_count'] = Article.objects.filter(author=self.object, is_published=True).count()
# return context


class UserAccountEdit(UpdateView):
    """
    Редактирование профиля пользователя
    Контекст:   object - содержит все поля модели пользователя (пример: {{ object.username }})
                form - содержит поле логина и пароля (пример : {{ form.username }}, или стандартно {{ form.as_p }})
    Имя шаблона: geekhubuser_update.html
    """
    model = GeekHubUser
    form_class = UserProfileEditForm
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(UserAccountEdit, self).get_context_data()
        context['hubs'] = Hub.objects.all()
        context['title'] = f'Профиль пользователя {self.object.username}'
        # TODO написать контекстные процессоры для количества статей
        context['user_drafts_count'] = Article.objects.filter(author=self.object, is_draft=True).count()
        context['user_articles_published_count'] = Article.objects.filter(author=self.object, is_published=True).count()
        return context

    def get_initial(self):
        """ Устанавливает начальные значения формы. """
        initial = super(UserAccountEdit, self).get_initial()
        initial['first_name'] = self.object.first_name
        initial['last_name'] = self.object.last_name
        initial['profile_photo'] = self.object.profile_photo
        initial['user_information'] = self.object.user_information
        initial['gender'] = self.object.gender
        initial['article_redactor'] = self.object.article_redactor
        return initial

    def get_success_url(self):
        return reverse_lazy('usersapp:modify', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        """ Сохраняет данные пользователя из формы и возвращает редирект на страницу профиля. """
        user = self.get_object()
        form_data = request.POST

        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.user_information = form_data['user_information']
        user.gender = form_data['gender']
        # TODO проработать формат сохранения даты в БД (если поле пустое вылетает ошибка)
        # user.birthday = form_data['birthday']
        user.article_redactor = form_data['article_redactor']
        user.save()

        super(UserAccountEdit, self).post(request)
        return HttpResponseRedirect(self.get_success_url())


class UserAccountDeleteView(DeleteView):
    """
    Удаление профиля пользователя
    Как и договаривались, вместо удаления, производим деактивацию
    Имя шаблона: geekhubuser_confirm_delete.html
    """
    model = GeekHubUser
    success_url = reverse_lazy('mainapp:index')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        print(user.is_active)
        return HttpResponseRedirect(self.success_url)


def verify(request, email, activate_key):
    """
    Верификация и активация пользователя по e-mail и активационному коду
    """
    try:
        user = GeekHubUser.objects.get(email=email)
        if user.activate_key == activate_key and not user.is_activate_key_expired():
            user.is_active = True
            user.activate_key = None
            user.save()
            auth.login(request, user)
            # ToDo: тут логируем что активация пользователя прошла успешно
        return HttpResponseRedirect('/auth/verify/')
    except Exception as e:
        # ToDo: тут логируем ошибку активации - {e.args}
        print(e, e.args)
        return HttpResponseRedirect('/auth/verify/')


def verification(request):
    return render(request, 'usersapp/verification.html')
