# Generated by Django 3.2.4 on 2021-07-22 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0001_initial'),
        ('commentsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsbranch',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.article'),
        ),
    ]
