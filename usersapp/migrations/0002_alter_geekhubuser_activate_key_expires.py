# Generated by Django 3.2.4 on 2021-07-19 17:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 18, 24, 23, 931168, tzinfo=utc), verbose_name='Время действия кода активации'),
        ),
    ]
