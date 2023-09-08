# Generated by Django 4.2.4 on 2023-09-08 15:21

import conflict.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('status', models.TextField(choices=[('active', 'Active'), ('closed', 'Closed')], default='active')),
                ('creator',
                 models.CharField(choices=[(1, 'Иванов'), (2, 'Петров'), (3, 'Сидоров')], default='by appointment',
                                  max_length=250)),
                ('respondent',
                 models.CharField(choices=[(1, 'Иванов'), (2, 'Петров'), (3, 'Сидоров')], default='by appointment',
                                  max_length=250)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_as_visible', models.BooleanField(default=False, verbose_name='As visible')),
                ('concluded_contract', models.BooleanField(default=False, verbose_name='Signed contract')),
                ('personal_data_processed',
                 models.BooleanField(default=False, verbose_name='Permission to process data')),
                ('respect_confidentiality', models.BooleanField(default=False, verbose_name='Respect confidentiality')),
                ('mediator',
                 models.CharField(choices=[(1, 'Иванов'), (2, 'Петров'), (3, 'Сидоров')], default='by appointment',
                                  max_length=250)),
                ('body_as_markdown', models.BooleanField(default=False, verbose_name='As markdown')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('closed_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Appeal',
                'verbose_name_plural': 'Appeal',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user',
                 models.CharField(choices=[(1, 'Иванов'), (2, 'Петров'), (3, 'Сидоров')], default='by appointment',
                                  max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('file_as_visible', models.BooleanField(default=False, verbose_name='As visible')),
                ('file_path', models.FileField(upload_to=conflict.models.user_directory_path)),
                ('conflict', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files',
                                               to='conflict.conflict')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conflict.documenttype')),
            ],
        ),
    ]