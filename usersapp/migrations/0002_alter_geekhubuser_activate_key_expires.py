# Generated by Django 3.2.4 on 2021-07-21 13:37

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
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 21, 14, 37, 26, 442392, tzinfo=utc), verbose_name='Время действия кода активации'),
        ),
    ]
