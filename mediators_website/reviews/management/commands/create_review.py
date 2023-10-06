from django.core.management.base import BaseCommand
from reviews.forms import ReviewForm
from user.models import BasicUser, Mediator
from faker import Faker
from random import randint
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class Command(BaseCommand):
    help = """
        Создание отзывов о медиаторах.
            -t, --total     Количество создаваемых отзывов
            -s, --symbols   Количество символов текста отзыва
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых юзеров')
        parser.add_argument('-s', '--symbols', type=int, help=u'Количество символов текста отзыва')

    def get_random_data(self, symbols):
        try:
            from_user = fake.random_choices(elements=BasicUser.objects.all(), length=1)[0]
            to_user = fake.random_choices(elements=Mediator.objects.all(), length=1)[0]
        except IndexError:
            raise ValueError('В базе нет пользователей. Выполни команду: python manage.py create_user')

        rating = randint(1, 5)
        text = fake.text(symbols)

        return {
            'to_user': to_user,
            'from_user': from_user,
            'rating': rating,
            'text': text,
        }

    def handle(self, *args, **options):
        total = options.get('total') or 1
        symbols = options.get('symbols') or 150

        for i in range(total):
            data = self.get_random_data(symbols=symbols)
            form = ReviewForm(data=data)
            if form.is_valid():
                form.save()
                print(f'Отзыв написан пользователем {data.get("from_user").firstname}')
            else:
                print(form.errors)