import uuid
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.mail import send_mail
from django.urls import reverse
from usersapp.models import GeekHubUser


def send_verify_mail(user):
    verify_link = reverse('usersapp:verify', args=[user.email, user.activate_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ' \
              f'ссылке: \n{settings.DOMAIN_NAME}{verify_link} '
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False,
                     auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'button3'}))
    # username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'button3'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'button3'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'button3'}))

    class Meta(object):
        model = GeekHubUser
        fields = ('username', 'email', 'password1', 'password2')

    # ToDo: Вот тут мне не нравится метод save, пришлось все забрать из родительского модуля
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        user.activate_key = uuid.uuid4().hex
        send_verify_mail(user)

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'button4"'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'button4"'}))


class UserProfileForm(UserChangeForm):
    class Meta:
        model = GeekHubUser
        fields = '__all__'


class UserProfileEditForm(UserChangeForm):
    class Meta:
        model = GeekHubUser
        fields = ['first_name', 'last_name', 'profile_photo', 'user_information', 'birthday', 'gender',
                  'article_redactor']
