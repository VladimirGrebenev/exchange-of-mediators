from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from signing.forms import UserRegisterForm
from user.models import User
from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class Command(BaseCommand):
    help = """
        Создание тестовых пользователей. По умолчанию создаются обычные юзеры
            -t, --total     Количество создаваемых пользователей
            -p, --password  Пароль для создаваемого пользователя
            -m, --mediator  Создавать медиатора
            -e, --email     Указать email. Будет добавлен порядковый номер создаваемого пользователя в бд
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых пользователей')
        parser.add_argument('-p', '--password', type=str, help='Пароль для user')
        parser.add_argument('-m', '--mediator', action='store_true', help='Создать медиатора')
        parser.add_argument('-e', '--email', type=str, help='Указать email')

    def get_random_user(self):
        gender = fake.random_choices(elements=('male', 'female'), length=1)[0]
        if gender == 'male':
            user = fake.first_name_male(), fake.last_name_male()
        else:
            user = fake.first_name_female(), fake.last_name_female()
        return user

    def handle(self, *args, **options):
        count = User.objects.count() + 1
        total = options.get('total') or 1
        password = options.get('password') or '123'
        mail = options.get('email') or 'mail'

        role = 'client'
        if options.get('mediator'):
            role = 'mediator'

        for i in range(count, count + total):
            firstname, lastname = self.get_random_user()
            data = {
                'firstname': firstname,
                'lastname': lastname,
                'password1': password,
                'password2': password,
                'role': role,
                'email': f'{mail}{i}@mail.ru',
            }
            form = UserRegisterForm(data=data)
            if form.is_valid():
                user = form.save(commit=False)
                new_group, _ = Group.objects.get_or_create(name={'client': 'user', 'mediator': 'mediator'}[role])
                user.groups.set([new_group])
                user.save()
                print(f'Создан {new_group}: {user.firstname}, Email: {user.email}')
