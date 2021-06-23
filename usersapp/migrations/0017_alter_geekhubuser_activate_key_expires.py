# Generated by Django 3.2.4 on 2021-06-21 05:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('usersapp', '0016_auto_20210620_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 21, 6, 50, 4, 594833, tzinfo=utc),
                                       verbose_name='Время действия кода активации'),
        ),
    ]
