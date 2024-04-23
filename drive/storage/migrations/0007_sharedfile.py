# Generated by Django 5.0.4 on 2024-04-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0006_remove_file_category_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True)),
                ('file_path', models.CharField(max_length=255)),
                ('is_public', models.BooleanField(default=False)),
            ],
        ),
    ]
