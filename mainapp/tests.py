import datetime
from django.test import TestCase
from django.core.management import call_command
from mainapp.models import Hub, Article
from usersapp.models import GeekHubUser


class TestUser(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')

    def test_mainpage_success(self):
        # Проверка открытия главной страницы
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='Главная :: Intergalactic Entertainment')


class TestHubModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Hub.objects.create(name='Мобильная разработка', description='Статьи о мобильной разработке')

    def test_name_label(self):
        hub = Hub.objects.get(id=1)
        field_label = hub._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
        field_label = hub._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_name_max_length(self):
        hub = Hub.objects.get(id=1)
        max_length = hub._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)

    def test_get_absolute_url(self):
        hub = Hub.objects.get(id=1)
        self.assertEquals(hub.get_absolute_url(), '/hub/1/')


class TestArticleModule(TestCase):

    @classmethod
    def setUpTestData(cls):
        GeekHubUser.objects.create_user('Agile449', 'pythonagile449@gmail.com', 'Geek@2021')
        user = GeekHubUser.objects.get(id=1)
        Hub.objects.create(name='Мобильная разработка', description='Статьи о мобильной разработке')
        hub = Hub.objects.get(id=1)
        Article.objects.create(id='00000000-0000-0000-0000-000000000001', title='Статья о мобильной разработке',
                               publication_date=datetime.date.today(),
                               is_published=True, author=user, hub=hub,
                               created_at=datetime.date.today(), is_draft=False, is_moderation_in_progress=False)

    def test_name_label(self):
        article = Article.objects.get(id='00000000-0000-0000-0000-000000000001')
        field_label = article._meta.verbose_name
        self.assertEquals(field_label, 'Статья')
        field_label = article.get_field('title')
        print(field_label)

    def test_get_absolute_url(self):
        article = Article.objects.get(id='00000000-0000-0000-0000-000000000001')
        self.assertEquals(article.get_absolute_url(), '/article/00000000-0000-0000-0000-000000000001/')