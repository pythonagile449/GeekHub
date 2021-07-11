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
    RU
    Главная страница приложения usersapp

    EN
    Usersapp main page view
    """

    return render(request, 'usersapp/index.html')


class RegistrationView(CreateView):
    '''
    RU
    Представление регистрации пользователя.
    Передаваемый контекст:

    EN
    View for user registration form
    Context passed:
    '''
    model = GeekHubUser
    form_class = RegistrationForm
    success_url = '/auth/verify/'


class AuthenticationView(LoginView):
    """
    RU
    Аутентификация пользователя
    Контекст: form, содержит поле логина и пароля (пример : {{ form.username }}, или стандартно {{ form.as_p }})
    Имя шаблона: login.html

    EN
    User authentication view
    Context: form, has fields for login and password (example: {{ form.username }} or {{ form.as_p }}
    Template name: login.html
    """
    form_class = LoginForm
    template_name = 'usersapp/login.html'


class UserLogoutView(LogoutView):
    """
    RU
    Выход из аккаунта
    Завершает текущий сеанс работы пользователя, с отображением страницы
    Имя шаблона: logout.html

    EN
    View for logout from the account
    Stops current user's session, displays the page
    Template name: logout.html
    """
    template_name = 'usersapp/logout.html'


class UserAccountEdit(UpdateView):
    """
    RU
    Редактирование профиля пользователя
    Контекст:   object - содержит все поля модели пользователя (пример: {{ object.username }})
                form - содержит поле логина и пароля (пример : {{ form.username }}, или стандартно {{ form.as_p }})
    Имя шаблона: geekhubuser_update.html

    EN
    User profile edit view
    Context:    object - contains all the fields of the model GeekHubUser (example: {{ object.username }}
                form - contains fields for login and password (example: {{ form.username }} or {{ form.as_p }}
    Template name: geekhubuser_update.html
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

    def get(self, request, *args, **kwargs):
        try:
            if request.user == GeekHubUser.objects.get(pk=kwargs['pk']):
                self.object = self.get_object()
                return super().get(request, *args, **kwargs)
            return render(request, template_name='mainapp/400.html')
        except Exception as e:
            return render(request, template_name='mainapp/400.html')


class UserAccountDeleteView(DeleteView):
    """
    RU
    Удаление профиля пользователя
    Как и договаривались, вместо удаления, производим деактивацию
    Имя шаблона: geekhubuser_confirm_delete.html

    EN
    View for users deletion
    As we agreed, we deactivate user instead of outright deletion
    Template name: geekhubuser_confirm_delete.html
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
    RU
    Верификация и активация пользователя по e-mail и активационному коду

    EN
    Verification of user via email and activation code
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
