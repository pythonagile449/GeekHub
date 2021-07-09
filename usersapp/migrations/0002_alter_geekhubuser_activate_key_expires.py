# Generated by Django 3.2.4 on 2021-07-08 06:56

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
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 8, 7, 56, 21, 662635, tzinfo=utc),
                                       verbose_name='Время действия кода активации'),
        ),
    ]
