# Generated by Django 4.2.4 on 2023-09-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conflict', '0003_document_delete_documenttype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conflict',
            name='category',
            field=models.TextField(choices=[('выбрать', 'выбрать'), ('корпоративный', 'корпоративный'), ('бизнес', 'бизнес'), ('семейный', 'семейный'), ('недвижимость', 'недвижимость'), ('наследство', 'наследство'), ('личный', 'личный')], default='Черновик', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='conflict',
            name='status',
            field=models.TextField(choices=[('В работе', 'В работе'), ('Завершен', 'Завершен'), ('Новый', 'Новый'), ('Черновик', 'Черновик')], default='Черновик', verbose_name='Статус'),
        ),
    ]
