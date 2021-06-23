from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from usersapp.models import GeekHubUser
from django.core.management import call_command


class TestUser(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = GeekHubUser.objects.create_superuser('GeekHubUser', 'admin@geekhub.ru', 'Geek@2021')
        self.user = GeekHubUser.objects.create_user('first_user', 'first_user@reqsoft.ru', 'Geek@2021')
        self.user_with__first_name = GeekHubUser.objects.create_user('second_user', 'second_user@reqsoft.ru',
                                                                     'Geek@2021', first_name='R2D2')

    def test_user_registration_success(self):
        # Проверка регистрации
        response = self.client.get('/auth/registration/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        # Задаем данные для регистрации
        new_user_data = {
            'username': 'BigBrother',
            'password1': 'Geek@2021',
            'password2': 'Geek@2021',
            'email': 'chehov@reqsoft.ru',
        }

        response = self.client.post('/auth/registration/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = GeekHubUser.objects.get(username=new_user_data['username'])
        # Проверяем верификацию пользователя по ссылке отправленной на email
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activate_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 302)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        # Аутентифицируемся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # Проверяем страницу аккаунта
        response = self.client.get(f'/auth/account/{new_user.pk}')
        self.assertContains(response, text=new_user_data['username'], status_code=200)

    def test_user_registration_error(self):
        # Задаем данные первого пользователя
        self.superuser = GeekHubUser.objects.create_user('GeekHubUser2', 'admin2@geekhub.ru', 'Geek@2021')
        # Задаем данные для регистрации другого пользователя с существующими username и email
        new_user_data = {
            'username': 'GeekHubUser2',
            'password1': 'Geek@2021',
            'password2': 'Geek@2021',
            'email': 'admin2@geekhub.ru',
        }
        response = self.client.post('/auth/registration/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='Пользователь с таким именем уже существует.', status_code=200)
        self.assertContains(response, text='Пользователь с таким E-mail уже существует.', status_code=200)

    def test_user_logout(self):
        # Задаем данные пользователя под кем зайдем
        self.client.login(username='first_user', password='Geek@2021')
        # Проводим аутентификацию
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        # Выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 200)
        # При корректном выходе проверяем переход на страницу входа
        response = self.client.get('/auth/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
