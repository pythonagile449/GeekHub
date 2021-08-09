from django.core.management.base import BaseCommand

from usersapp.models import GeekHubUser, UserNotificationSettings


class Command(BaseCommand):

    def handle(self, *args, **options):
        if options['create']:
            try:
                users = GeekHubUser.objects.all()
                for user in users:
                    UserNotificationSettings.objects.get_or_create(user=user)
                print("Настройки уведомлений пользователей довавлены")
            except Exception as e:
                print(f"Ошибка: {e} при создании настроек уведомлений")

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--create',
            action='store_true',
            default=False,
            help='Создание настроек уведомлений для текущих пользователей'
        )
