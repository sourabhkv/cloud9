# Generated by Django 5.0.1 on 2024-04-19 14:49

import storage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=storage.models.user_directory_path),
        ),
    ]
