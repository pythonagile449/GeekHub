# Generated by Django 3.2.4 on 2021-06-28 04:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0038_alter_geekhubuser_activate_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 5, 32, 4, 617983, tzinfo=utc), verbose_name='Время действия кода активации'),
        ),
    ]