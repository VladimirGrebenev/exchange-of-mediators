# Generated by Django 4.2.5 on 2023-09-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_delete_document_delete_documenttype"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="photo",
            field=models.FilePathField(blank=True, null=True, path="mediators_photo/"),
        ),
        migrations.AddField(
            model_name="user",
            name="rate",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="summary",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
