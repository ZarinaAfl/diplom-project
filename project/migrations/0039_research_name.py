# Generated by Django 2.2.9 on 2020-05-02 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0038_auto_20200428_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='name',
            field=models.CharField(default='test', max_length=255),
        ),
    ]
