# Generated by Django 4.2.4 on 2023-10-03 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conflict', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conflict',
            name='is_all_visible',
        ),
        migrations.RemoveField(
            model_name='conflict',
            name='language',
        ),
        migrations.RemoveField(
            model_name='conflict',
            name='language_level',
        ),
        migrations.RemoveField(
            model_name='conflict',
            name='mediators_level',
        ),
        migrations.RemoveField(
            model_name='conflict',
            name='prise',
        ),
        migrations.RemoveField(
            model_name='conflict',
            name='respondents',
        ),
        migrations.RemoveField(
            model_name='conflict',
            name='status',
        ),
    ]
