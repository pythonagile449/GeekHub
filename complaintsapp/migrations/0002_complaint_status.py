# Generated by Django 3.2.4 on 2021-07-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('complaintsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('A', 'Approved'), ('M', 'Moderating'), ('D', 'Discarded')], default='M',
                                   max_length=1, verbose_name='Статус'),
        ),
    ]
