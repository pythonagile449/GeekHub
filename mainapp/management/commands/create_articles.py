import random
from django.core.management import BaseCommand
from faker import Faker
from mdgen import MarkdownPostProvider

from mainapp.models import Article, Hub
from usersapp.models import GeekHubUser


class Command(BaseCommand):
    help = 'Создает 10 статей с выбранным статусом через faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--drafts',
            action='store_true',
            default=False,
            help='Создание черновиков'
        )
        parser.add_argument(
            '-m',
            '--moderation',
            action='store_true',
            default=False,
            help='Создание статей на модерации'
        )
        parser.add_argument(
            '-p',
            '--published',
            action='store_true',
            default=False,
            help='Создание опубликованных статей'
        )

    def handle(self, *args, **options):
        faker = Faker(['ru-RU'])
        faker.add_provider(MarkdownPostProvider)

        users_ids_list = GeekHubUser.objects.all().values_list('id', flat=True)
        hubs_ids_list = Hub.objects.all().values_list('id', flat=True)
        print(users_ids_list)
        print(hubs_ids_list)

        for _ in range(10):
            try:
                new_article = Article.objects.create(
                    title=faker.sentence(nb_words=10),
                    contents=faker.post(size='medium')+'<MD>',
                    short_description=faker.sentence(nb_words=3),
                    created_at=faker.date_between(start_date='-1y', end_date='today'),
                    publication_date=faker.date_between(start_date='-1m', end_date='today'),
                    hub=Hub.objects.get(id=random.choice(hubs_ids_list)),
                    author=GeekHubUser.objects.get(id=random.choice(users_ids_list)),
                )

                if options['moderation']:
                    new_article.is_draft = False
                    new_article.is_moderation_in_progress = True
                if options['published']:
                    new_article.is_draft = False
                    new_article.is_moderation_in_progress = False
                    new_article.is_published = True

                new_article.save()
                print(f'Успешно создана статья, id: {new_article.id}')
            except Exception as e:
                print(f'Создание статьи завершилось ошибкой: {e}')
