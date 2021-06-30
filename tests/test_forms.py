from django.test import TestCase
from usersapp.models import GeekHubUser
from usersapp.forms import LoginForm, RegistrationForm


class TestGeekHubUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        GeekHubUser.objects.create_user('Agile449', 'pythonagile449@gmail.com', 'Geek@2021')

    def test_register_exists_user(self):
        # Проверка введенных корректных данных, но уже имеющихся в базе данных
        form_data = {'username': 'Agile449', 'email': 'pythonagile449@gmail.com', 'password1': 'Geek@2021',
                     'password2': 'Geek@2021'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_new_user(self):
        # Проверка введенных корректных данных
        form_data = {'username': 'GeekBrains', 'email': 'geeks@gmail.com', 'password1': 'Geek@2021',
                     'password2': 'Geek@2021'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_user_invalid_data(self):
        # Проверка введенных некорректных данных (ошибка в email)
        form_data = {'username': 'User1', 'email': 'pythonagile449gmail.com', 'password1': 'Geek@2021',
                     'password2': 'Geek@2021'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_user(self):
        # Проверка аутентификации пользователя
        form_data = {'username': 'Agile449', 'password': 'Geek@2021'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
