# Generated by Django 2.2.9 on 2020-02-12 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20200212_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paramvalue',
            name='file_name',
        ),
    ]
