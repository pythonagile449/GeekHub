import random
import markdown
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

        html_text = '<p>Как-то раз, крася и двигая кнопки, я заметил, что ресайклер вью на одном из наших экранов ' \
                    'немного проседал по отрисовке при активном скролле из-за большого разнообразия ' \
                    '<code>viewType</code> (и, как следствие, частого создания новых вьюхолдеров), и, глядя на это, ' \
                    'вспомнил о <a href="https://medium.com/google-developers/recyclerview-prefetch-c2f269075710">' \
                    'старой статье Chet Haase</a> про то, как появилась возможность нагружать ресайклер работой по ' \
                    'префетчингу элементов в моменты простоя мэйн трэда. Но мне показалось этого мало, и захотелось ' \
                    'создавать элементы в моменты простоя...не мэйн трэда.</p>'

        for i in range(10):
            md_text = faker.post(size='medium')
            try:
                new_article = Article.objects.create(
                    title=faker.sentence(nb_words=10),
                    short_description=faker.sentence(nb_words=3),
                    created_at=faker.date_between(start_date='-1y', end_date='today'),
                    publication_date=faker.date_between(start_date='-1m', end_date='today'),
                    hub=Hub.objects.get(id=random.choice(hubs_ids_list)),
                    author=GeekHubUser.objects.get(id=random.choice(users_ids_list)),
                )

                if not i % 2:
                    new_article.contents = markdown.markdown(md_text)
                else:
                    new_article.contents = html_text

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
