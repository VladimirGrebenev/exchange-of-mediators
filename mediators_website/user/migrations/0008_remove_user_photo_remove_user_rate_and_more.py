# Generated by Django 4.2.5 on 2023-09-21 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_user_photo_user_rate_user_summary"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="user",
            name="rate",
        ),
        migrations.RemoveField(
            model_name="user",
            name="summary",
        ),
    ]
