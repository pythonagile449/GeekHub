# Generated by Django 3.2.4 on 2021-07-29 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleviews',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_view', to='mainapp.article'),
        ),
    ]
