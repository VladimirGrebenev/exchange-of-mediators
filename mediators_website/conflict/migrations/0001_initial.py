# Generated by Django 4.2.4 on 2023-10-06 07:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Conflict",
            fields=[
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("В работе", "В работе"),
                            ("Завершен", "Завершен"),
                            ("Новый", "Новый"),
                        ],
                        default="Новый",
                        null=True,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "category",
                    models.TextField(
                        choices=[
                            ("не выбрано", "не выбрано"),
                            ("корпоративный", "корпоративный"),
                            ("бизнес", "бизнес"),
                            ("семейный", "семейный"),
                            ("недвижимость", "недвижимость"),
                            ("наследство", "наследство"),
                            ("личный", "личный"),
                        ],
                        default="не выбрано",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "fixed_price",
                    models.CharField(max_length=256, null=True, verbose_name="Цена"),
                ),
                (
                    "decide_time",
                    models.TextField(
                        choices=[
                            ("не выбрано", "не выбрано"),
                            ("1 День", "1 День"),
                            ("2 Дня", "2 Дня"),
                            ("3 Дня", "3 Дня"),
                            ("1 Неделя", "1 Неделя"),
                        ],
                        default="не выбрано",
                        verbose_name="Время на решение",
                    ),
                ),
                (
                    "country",
                    models.CharField(max_length=256, null=True, verbose_name="Страна"),
                ),
                (
                    "city",
                    models.CharField(max_length=256, null=True, verbose_name="Город"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=256, verbose_name="Заголовок обращения"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("deleted", models.BooleanField(default=False, editable=False)),
                ("closed_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Conflict",
                "verbose_name_plural": "Conflict",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("file_path", models.FileField(null=True, upload_to="documents_users")),
                (
                    "is_all_visible",
                    models.BooleanField(default=False, verbose_name="Виден всем?"),
                ),
                (
                    "conflict",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="conflict.conflict",
                        verbose_name="Обращение",
                    ),
                ),
            ],
        ),
    ]
