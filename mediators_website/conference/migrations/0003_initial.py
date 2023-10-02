# Generated by Django 4.2.4 on 2023-09-25 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferences',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conferences',
            name='invated_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]