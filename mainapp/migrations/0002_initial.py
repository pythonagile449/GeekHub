# Generated by Django 3.2.4 on 2021-07-07 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
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
    ]
