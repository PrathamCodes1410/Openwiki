# Generated by Django 4.1.4 on 2023-01-25 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0002_user_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_name',
        ),
    ]