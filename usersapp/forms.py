import uuid
from datetime import timedelta, datetime

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms import ModelForm
from django.urls import reverse
from django.utils.timezone import now

from usersapp.models import GeekHubUser, UserNotificationSettings


def send_verify_mail(user):
    verify_link = reverse('usersapp:verify', args=[user.email, user.activate_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ' \
              f'ссылке: \n{settings.DOMAIN_NAME}{verify_link} '
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False,
                     auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'button3'}))
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
        user.activate_key_expires = now() + timedelta(hours=1)
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


class UserProfileDetailForm:
    class Meta:
        model = GeekHubUser
        fields = '__all__'


class UserProfileEditForm(ModelForm):
    # def __init__(self, notification_settings=None, *args, **kwargs):
    #     self.user_notification_settings = notification_settings
    #     super(UserProfileEditForm, self).__init__(*args, **kwargs)

    other = 'O'
    male = 'M'
    female = 'W'

    GENDER_CHOISES = (
        (other, 'другой'),
        (male, 'мужской'),
        (female, 'женский'),
    )

    md_editor = 'MD'
    ckeditor = 'CK'

    REDACTOR_CHOISES = (
        (md_editor, 'markdown'),
        (ckeditor, 'сkeditor'),
    )

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'placeholder'}), required=False)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'placeholder'}), required=False)
    user_information = forms.CharField(label='О себе', widget=forms.Textarea(attrs={'class': 'placeholder'}),
                                       required=False)
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'placeholder',
                                                                                    'type': 'date',
                                                                                    'min': '1920-01-01'}),
                               required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOISES, widget=forms.Select(attrs={'class': 'placeholder'}),
                               required=False)
    article_redactor = forms.ChoiceField(choices=REDACTOR_CHOISES, widget=forms.Select(attrs={'class': 'placeholder'}),
                                         required=False)
    profile_photo = forms.ImageField(label='Фото', widget=forms.FileInput(attrs={'class': '', 'required': False, }),
                                     required=False)

    notify_article_comments = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'notification-checkbox'}), required=False,
        label='Комментарии к статьям', label_suffix='')
    notify_article_change_status = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'notification-checkbox'}), required=False,
        label='Изменении статуса статьи', label_suffix='')
    notify_moderator_messages = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'notification-checkbox'}), required=False,
        label='Сообщения при модерации', label_suffix='')
    notify_complaints_against_article_status = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'notification-checkbox'}), required=False,
        label='Статус жалоб на статью', label_suffix='')
    notify_complaints_against_comment_status = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'notification-checkbox'}), required=False,
        label='Статус жалоб на комментарии', label_suffix='')

    def save(self, commit=True):
        user = super(UserProfileEditForm, self).save(commit=False)
        print(user)
        user_notify_settings = UserNotificationSettings.objects.get(user=user)
        print(user_notify_settings)
        user_notify_settings.notify_article_comments = self.cleaned_data['notify_article_comments']
        user_notify_settings.notify_article_change_status = self.cleaned_data['notify_article_change_status']
        user_notify_settings.notify_moderator_messages = self.cleaned_data['notify_moderator_messages']
        user_notify_settings.notify_complaints_against_article_status = self.cleaned_data[
            'notify_complaints_against_article_status']
        user_notify_settings.notify_complaints_against_comment_status = self.cleaned_data[
            'notify_complaints_against_comment_status']
        user_notify_settings.save()
        return user

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        minimal_age_years = 7

        if birthday is not None:
            user_age = int((datetime.now().date() - birthday).days / 365.25)
            if (datetime.now().date() - birthday).days < 0:
                raise ValidationError('Похоже вы еще не родились')
            if 0 <= user_age < minimal_age_years:
                raise ValidationError('Вы слишком молоды')
            if user_age > 100:
                raise ValidationError('Вам более 100 лет')

        return birthday

    class Meta:
        model = GeekHubUser
        fields = ['first_name', 'last_name', 'profile_photo', 'user_information', 'birthday', 'gender',
                  'article_redactor']
