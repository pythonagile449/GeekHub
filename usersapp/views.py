from django.contrib import auth
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from usersapp.models import GeekHubUser
from usersapp.forms import RegistrationForm, LoginForm, UserProfileForm


def main(request):
    """
    Главная страница приложения usersapp
    """
    return render(request, 'usersapp\index.html')


class RegistrationView(CreateView):
    '''
    Представление регистрации пользователя.
    Передаваемый контекст:
    '''
    model = GeekHubUser
    form_class = RegistrationForm
    success_url = '/auth/'


class AuthenticationView(LoginView):
    """
    Аутентификация пользователя
    Контекст: form, содержит поле логина и пароля (пример : {{ form.username }}, или стандартно {{ form.as_p }})
    Имя шаблона: login.html
    """
    form_class = LoginForm
    template_name = 'usersapp\login.html'


class UserLogoutView(LogoutView):
    """
    Выход из аккаунта
    Завершает текущий сеанс работы пользователя, с отображением страницы
    Имя шаблона: logout.html
    """
    template_name = 'usersapp\logout.html'


class UserAccountView(DetailView):
    """
    Профиль пользователя
    Контекст: object, содержит все поля модели пользователя (пример: {{ object.username }})
    Имя шаблона: geekhubuser_detail.html
    """
    model = GeekHubUser
    form_class = UserProfileForm


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
            return render(request, 'usersapp/verification.html')
        else:
            # ToDo: тут логируем что пользователь уже прошел активацию
            return render(request, 'usersapp/verification.html')
    except Exception as e:
        # ToDo: тут логируем ошибку активации - {e.args}
        return HttpResponseRedirect(reverse('usersapp:index'))
