from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from mainapp.models import Hub


class Command(BaseCommand):
    help = 'Создает хабы из списка'
    hubs_list = ['Дизайн', 'Веб-разработка', 'Мобильная разработка', 'Маркетинг']
    hubs_created = []

    def handle(self, *args, **options):
        for hub_name in self.hubs_list:
            try:
                hub = Hub.objects.create(name=hub_name)
                self.hubs_created.append(hub)
            except IntegrityError:
                print(f'Ошибка создания хаба, хаб с имененем {hub_name} уже сужествует.')
        print(f'Успешно создано {len(self.hubs_created)} хаба(ов)')
