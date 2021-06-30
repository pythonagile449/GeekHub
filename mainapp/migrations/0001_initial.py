# Generated by Django 3.2.4 on 2021-06-30 19:11

import ckeditor.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('front_image', models.ImageField(blank=True, upload_to='article_front_img')),
                ('contents', ckeditor.fields.RichTextField(blank=True)),
                ('short_description', models.CharField(blank=True, max_length=256)),
                ('publication_date', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('is_draft', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_moderation_in_progress', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Хаб',
                'verbose_name_plural': 'Хабы',
            },
        ),
    ]
