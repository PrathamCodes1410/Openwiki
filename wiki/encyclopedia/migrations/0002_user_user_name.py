# Generated by Django 4.1.4 on 2023-01-25 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
