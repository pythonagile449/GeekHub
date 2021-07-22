# Generated by Django 3.2.4 on 2021-07-22 20:18

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.operations import BtreeGinExtension


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        BtreeGinExtension(),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='hub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.hub'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='mainapp_art_title_85435d_gin'),
        ),
    ]
