# Generated by Django 3.2.4 on 2021-07-26 19:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='reason_for_reject',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Причина снятия с публикации'),
        ),
    ]