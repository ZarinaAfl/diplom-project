# Generated by Django 2.2.9 on 2020-02-09 07:04

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20200208_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paramvalue',
            name='file',
            field=models.FileField(upload_to='files'),
        ),
        migrations.AlterField(
            model_name='paramvalue',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media/images'), upload_to=''),
        ),
    ]
