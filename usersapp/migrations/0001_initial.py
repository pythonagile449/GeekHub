# Generated by Django 3.2.4 on 2021-07-21 16:59

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockingByIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес')),
                ('failed_attempts', models.IntegerField(default=0, verbose_name='Неудачных попыток')),
                ('time_unblock', models.DateTimeField(blank=True, verbose_name='Время разблокировки')),
                ('blocking_status', models.BooleanField(default=False, verbose_name='Статус блокировки')),
            ],
            options={
                'verbose_name': 'Блокировку по IP',
                'verbose_name_plural': 'Блокировки по IP',
                'db_table': 'BlockingByIp',
            },
        ),
        migrations.CreateModel(
            name='GeekHubUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activate_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='Код активации')),
                ('activate_key_expires', models.DateTimeField(default=datetime.datetime(2021, 7, 21, 17, 59, 8, 105568, tzinfo=utc), verbose_name='Время действия кода активации')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('profile_photo', models.ImageField(blank=True, upload_to='media', verbose_name='Фотография профиля')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('user_information', models.CharField(blank=True, default='', max_length=512, verbose_name='Обо мне')),
                ('gender', models.CharField(choices=[('O', 'другой'), ('M', 'мужской'), ('W', 'женский')], default='O', max_length=1, verbose_name='Пол')),
                ('article_redactor', models.CharField(choices=[('MD', 'markdown'), ('CK', 'сkeditor')], default='CK', max_length=2, verbose_name='Редактор статей')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
