# Generated by Django 4.2.4 on 2023-10-03 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conflict', '0003_conflict_is_all_visible_conflict_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conflict',
            name='status',
        ),
    ]
