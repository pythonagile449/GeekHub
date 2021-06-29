# Generated by Django 3.2.4 on 2021-06-29 13:06

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_merge_0003_alter_article_id_0010_article_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='contents',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
