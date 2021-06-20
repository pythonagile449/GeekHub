# Generated by Django 3.2.4 on 2021-06-19 20:27

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
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 21, 20, 27, 20, 452999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='geekhubuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Код активации'),
        ),
    ]
