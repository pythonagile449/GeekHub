# Generated by Django 3.2.4 on 2021-06-22 14:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0022_alter_geekhubuser_activate_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 15, 52, 53, 299109, tzinfo=utc), verbose_name='Время действия кода активации'),
        ),
    ]
