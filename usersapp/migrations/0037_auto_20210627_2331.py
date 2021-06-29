# Generated by Django 3.2.4 on 2021-06-27 20:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0036_alter_geekhubuser_activate_key_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='geekhubuser',
            name='article_redactor',
            field=models.CharField(choices=[('MD', 'markdown'), ('CK', 'сkeditor')], default='CK', max_length=8, verbose_name='Редактор статей'),
        ),
        migrations.AlterField(
            model_name='geekhubuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 21, 31, 34, 786887, tzinfo=utc), verbose_name='Время действия кода активации'),
        ),
    ]
