# Generated by Django 3.2.4 on 2021-07-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaintsapp', '0002_complaint_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='reason_for_rejection',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Причина отклонения'),
        ),
    ]