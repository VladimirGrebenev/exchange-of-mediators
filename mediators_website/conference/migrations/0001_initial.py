# Generated by Django 4.2.5 on 2023-09-16 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("conflict", "0003_document_delete_documenttype_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conferences",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("scheduled_date", models.DateTimeField()),
                (
                    "file_path",
                    models.FilePathField(blank=True, null=True, path="conflicts_doc/"),
                ),
                (
                    "conflict_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="conflict.conflict",
                    ),
                ),
                (
                    "initiator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("invated_user", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
