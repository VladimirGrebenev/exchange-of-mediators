from django.core.management.base import BaseCommand
from conflict.forms import ConflictForm
from user.models import BasicUser
from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class Command(BaseCommand):
    help = """
        Создание конфликтов.
            -t, --total     Количество создаваемых конфликтов
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых конфликтов')

    def get_random_data(self):
        try:
            creator = fake.random_choices(elements=BasicUser.objects.all(), length=1)[0]
        except IndexError:
            raise ValueError('В базе нет пользователей. Выполни команду: python manage.py create_user')
        title = fake.text(80)
        category = fake.random_choices(
            elements=['корпоративный', 'бизнес', 'семейный', 'недвижимость', 'наследство'],
            length=1
        )[0]
        fixed_price = fake.random_number(digits=4)
        decide_time = fake.random_choices(
            elements=['1 День', '2 Дня', '3 Дня', '1 Неделя'],
            length=1
        )[0]
        city = fake.city_name()
        description = fake.text(500)

        return {
            'creator': creator,
            'title': title,
            'category': category,
            'fixed_price': fixed_price,
            'decide_time': decide_time,
            'country': 'Россия',
            'city': city,
            'description': description,
        }

    def handle(self, *args, **options):
        total = options.get('total') or 1

        for i in range(total):
            data = self.get_random_data()
            form = ConflictForm(data=data)
            if form.is_valid():
                form.save()
                print(f'Конфликт создан пользователем {data.get("creator").firstname}')
            else:
                print(form.errors)
