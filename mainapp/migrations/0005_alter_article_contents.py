# Generated by Django 3.2.4 on 2021-06-28 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_article_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='contents',
            field=models.TextField(blank=True),
        ),
    ]