# Generated by Django 3.2.4 on 2021-07-13 13:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0013_alter_geekhubuser_activate_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 14, 58, 42, 80123, tzinfo=utc), verbose_name='Время действия кода активации'),
        ),
    ]
