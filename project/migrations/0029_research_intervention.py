# Generated by Django 2.2.9 on 2020-03-09 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_auto_20200309_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='intervention',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='research_interv', to='project.Intervention', verbose_name='Исследование интервенции'),
        ),
    ]
