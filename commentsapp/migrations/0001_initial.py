# Generated by Django 3.2.4 on 2021-07-15 16:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_id', models.UUIDField(default=uuid.uuid4)),
                ('description', models.TextField(blank=True, verbose_name='Текст комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('hash_view', models.CharField(blank=True, max_length=256)),
                ('is_moderation', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'abstract': False,
            },
        ),
    ]
