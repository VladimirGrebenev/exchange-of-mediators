# Generated by Django 4.2.5 on 2023-09-27 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="additionalinfo",
            name="type",
        ),
    ]
