from django.core.management.base import BaseCommand
from conflict.management.commands.create_response import CreateResponse
from conflict.management.commands.create_conflict import CreateConflict
from user.management.commands.create_user import CreateUser
from user.models import User
from reviews.management.commands.create_review import CreateReview

from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class Command(BaseCommand):
    help = """
        Принимает один позиционный аргумент - число создаваемых сущностей 
        моделей User, Conflict, Review, ConflictResponse.
            Пример: python manage.py create_data 10
        
        Также отдельно каждую из указанных таблиц можно заполнить командами:
            - create_user;
            - create_conflict;
            - create_review;
            - create_response.
            
            Подробности: help по каждой из команд (python manage.py create_user --help)
    """

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Число создаваемых записей в таблицах')

    def handle(self, *args, **options):
        total = options.get('total') or 1
        count = User.objects.count() + 1

        green = '\033[92m'
        default = '\033[0m'

        print(green + 'Create users'.center(100, '=') + default)
        for i in range(count, total + count):
            user = CreateUser()
            user.create(password='123', role='client', num=i, username='user', server='mail.ru')

        print()
        print(green + 'Create mediators'.center(100, '=') + default)
        for i in range(count, total + count):
            mediator = CreateUser()
            mediator.create(password='123', role='mediator', num=i, username='mediator', server='mail.ru')

        print()
        print(green + 'Create conflicts'.center(100, '=') + default)
        for i in range(total):
            conflict = CreateConflict()
            conflict.create()

        print()
        print(green + 'Create reviews'.center(100, '=') + default)
        for i in range(total):
            review = CreateReview()
            review.create(symbols=150)

        print()
        print(green + 'Create responses'.center(100, '=') + default)
        for i in range(total):
            response = CreateResponse()
            response.create()
