from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from conflict.models import Conflict
from conflict.forms import ConflictForm, ResponseForm
from user.models import User, BasicUser, Mediator

from signing.forms import UserRegisterForm
from reviews.forms import ReviewForm

from random import randint

from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Укажи число и увидишь результат')

    def create_user(self, num, role):
        gender = fake.random_choices(elements=('male', 'female'), length=1)[0]
        if gender == 'male':
            firstname, lastname = fake.first_name_male(), fake.last_name_male()
        else:
            firstname, lastname = fake.first_name_female(), fake.last_name_female()

        data = {
            'firstname': firstname,
            'lastname': lastname,
            'password1': '123',
            'password2': '123',
            'role': 'client',
            'email': f'{role}{num}@mail.ru',
        }
        form = UserRegisterForm(data=data)
        if form.is_valid():
            user = form.save(commit=False)
            new_group, _ = Group.objects.get_or_create(name=role)
            user.groups.set([new_group])
            user.save()
            print(f'Создан {new_group}: {user.firstname}, Email: {user.email}')

    def create_conflict(self):
        creator = fake.random_choices(elements=BasicUser.objects.all(), length=1)[0]
        title = fake.text(randint(50, 80))
        category = fake.random_choices(
            elements=['корпоративный', 'бизнес', 'семейный', 'недвижимость', 'наследство'],
            length=1
        )[0]
        fixed_price = randint(50, 5000)
        decide_time = fake.random_choices(
            elements=['1 День', '2 Дня', '3 Дня', '1 Неделя'],
            length=1
        )[0]
        city = fake.city_name()
        description = fake.text(randint(300, 500))

        data = {
            'creator': creator,
            'title': title,
            'category': category,
            'fixed_price': fixed_price,
            'decide_time': decide_time,
            'country': 'Россия',
            'city': city,
            'description': description,
        }
        form = ConflictForm(data=data)
        if form.is_valid():
            form.save()
            print(f'Конфликт создан пользователем {data.get("creator").firstname}')

    def create_review(self):
        from_user = fake.random_choices(elements=BasicUser.objects.all(), length=1)[0]
        to_user = fake.random_choices(elements=Mediator.objects.all(), length=1)[0]
        rating = randint(1, 5)
        text = fake.text(randint(150, 500))

        data = {
            'to_user': to_user,
            'from_user': from_user,
            'rating': rating,
            'text': text,
        }

        form = ReviewForm(data=data)
        if form.is_valid():
            form.save()
            print(f'Отзыв написан пользователем {data.get("from_user").firstname}')

    def create_response(self):
        conflict = fake.random_choices(elements=Conflict.objects.all(), length=1)[0]
        mediator = fake.random_choices(elements=Mediator.objects.all(), length=1)[0]
        rate = fake.random_number(digits=4)
        time_for_conflict = fake.random_number(digits=1)
        comment = fake.text(150)

        data = {
            'conflict': conflict,
            'mediator': mediator,
            'rate': rate,
            'time_for_conflict': time_for_conflict,
            'comment': comment,
        }
        form = ResponseForm(data=data)
        if form.is_valid():
            form.save()
            print(f'Отклик на конфликт {data.get("conflict").title[:10]}... создан медиатором {data.get("mediator").firstname}')

    def handle(self, *args, **options):
        total = options.get('total') or 1
        count = User.objects.count() + 1

        green = '\033[92m'
        default = '\033[0m'

        print(green + 'Create users'.center(100, '=') + default)
        for i in range(count, total + count):
            self.create_user(i, 'user')

        print()
        print(green + 'Create mediators'.center(100, '=') + default)
        for i in range(count, total + count):
            self.create_user(i, 'mediator')

        print()
        print(green + 'Create conflicts'.center(100, '=') + default)
        for i in range(total):
            self.create_conflict()

        print()
        print(green + 'Create reviews'.center(100, '=') + default)
        for i in range(total):
            self.create_review()

        print()
        print(green + 'Create responses'.center(100, '=') + default)
        for i in range(total):
            self.create_response()
