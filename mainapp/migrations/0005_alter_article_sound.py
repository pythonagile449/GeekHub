# Generated by Django 3.2.4 on 2021-07-29 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_article_sound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='sound',
            field=models.ImageField(blank=True, upload_to='media', verbose_name='Фотография профиля'),
        ),
    ]