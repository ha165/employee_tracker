# Generated by Django 3.2.16 on 2024-11-21 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='date_joined',
        ),
    ]
