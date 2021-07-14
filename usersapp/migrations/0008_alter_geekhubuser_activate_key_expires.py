# Generated by Django 3.2.4 on 2021-07-14 19:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('usersapp', '0007_alter_geekhubuser_activate_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 14, 20, 34, 15, 616496, tzinfo=utc),
                                       verbose_name='Время действия кода активации'),
        ),
    ]
