# Generated by Django 3.2.4 on 2021-07-27 08:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_articleviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleviews',
            name='view_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 7, 27, 8, 40, 9, 863607, tzinfo=utc)),
            preserve_default=False,
        ),
    ]