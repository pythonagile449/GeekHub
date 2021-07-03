from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView

from usersapp.models import GeekHubUser
from usersapp.forms import RegistrationForm, LoginForm, UserProfileEditForm


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


class UserAccountEdit(UpdateView):
    """
    Редактирование профиля пользователя
    Контекст:   object - содержит все поля модели пользователя (пример: {{ object.username }})
                form - содержит поле логина и пароля (пример : {{ form.username }}, или стандартно {{ form.as_p }})
    Имя шаблона: geekhubuser_update.html
    """
    model = GeekHubUser
    template_name_suffix = '_update'
    fields = ['first_name', 'last_name', 'profile_photo', 'user_information', 'article_redactor', 'gender']

    def get_form_class(self):
        return UserProfileEditForm

    def get_context_data(self, **kwargs):
        context = super(UserAccountEdit, self).get_context_data()
        context['title'] = f'Профиль пользователя {self.object.username}'
        return context

    def get_success_url(self):
        return reverse_lazy('usersapp:modify', kwargs={'pk': self.object.id})


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
