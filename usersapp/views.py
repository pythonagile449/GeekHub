from urllib.parse import urlparse

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.http import is_safe_url, urlunquote
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView

from usersapp.models import GeekHubUser, BlockingByIp
from usersapp.forms import RegistrationForm, LoginForm, UserProfileEditForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_next_url(request):
    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, host=request.get_host()):
        next = '/'
    return next


def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = LoginForm
    return context


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

    def post(self, request):
        # забираем данные формы авторизации из запроса
        form = LoginForm(request, data=request.POST)

        # забираем IP адрес из запроса
        ip = get_client_ip(request)
        # получаем или создаём новую запись об IP, с которого вводится пароль, на предмет блокировки
        obj, created = BlockingByIp.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )

        # если IP заблокирован и время разблокировки не настало
        if obj.blocking_status is True and obj.time_unblock > timezone.now():
            context = create_context_username_csrf(request)
            if obj.failed_attempts == 3 or obj.failed_attempts == 6:
                # то открываем страницу с сообщением о блокировки на 15 минут при 3 и 6 неудачных попытках входа
                return render('accounts/block_15_minutes.html', context=context)
            elif obj.failed_attempts == 9:
                # или открываем страницу о блокировке на 24 часа, при 9 неудачных попытках входа
                return render('accounts/block_24_hours.html', context=context)
        elif obj.blocking_status is True and obj.time_unblock < timezone.now():
            # если IP заблокирован, но время разблокировки настало, то разблокируем IP
            obj.blocking_status = False
            obj.save()

        # если пользователь ввёл верные данные, то авторизуем его и удаляем запись о блокировке IP
        if form.is_valid():
            auth.login(request, form.get_user())
            obj.delete()

            next = urlparse(get_next_url(request)).path
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            return redirect(next)
        else:
            # иначе считаем попытки и устанавливаем время разблокировки и статус блокировки
            obj.failed_attempts += 1
            if obj.failed_attempts == 3 or obj.failed_attempts == 6:
                obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
                obj.blocking_status = True
            elif obj.failed_attempts == 9:
                obj.time_unblock = timezone.now() + timezone.timedelta(1)
                obj.blocking_status = True
            elif obj.failed_attempts > 9:
                obj.failed_attempts = 1
            obj.save()

        context = create_context_username_csrf(request)
        context['login_form'] = form

        return render('accounts/login.html', context=context)


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
