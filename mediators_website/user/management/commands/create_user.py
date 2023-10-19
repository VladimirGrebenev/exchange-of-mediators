from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from signing.forms import UserRegisterForm
from user.models import User, Mediator, BasicUser
from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class CreateUser:
    def get_random_user(self):
        gender = fake.random_choices(elements=('male', 'female'), length=1)[0]
        if gender == 'male':
            user = fake.first_name_male(), fake.last_name_male()
        else:
            user = fake.first_name_female(), fake.last_name_female()
        return user

    def create(self, password, role, username, num, server):
        firstname, lastname = self.get_random_user()
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'password1': password,
            'password2': password,
            'role': role,
            'email': f'{username}{num}@{server}',
        }
        form = UserRegisterForm(data=data)
        if form.is_valid():
            user = form.save(commit=False)
            new_group, _ = Group.objects.get_or_create(name={'client': 'user', 'mediator': 'mediator'}[role])
            user.groups.set([new_group])
            user.save()
            print(f'Создан {new_group}: {user.firstname}, Email: {user.email}')


class Command(BaseCommand):
    help = """
        Создание тестовых пользователей в базе данных
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых пользователей. По умолчанию 1')
        parser.add_argument('-p', '--password', type=str, help='Пароль для user. По умолчанию пароль "123"')
        parser.add_argument('-m', '--mediator', action='store_true', help='Создать медиатора. Без указания этого флага '
                                                                          'создается клиент')
        parser.add_argument('-e', '--email', type=str, help='Указать email. К имени пользователя почты будет добавлен '
                                                            'порядковый номер созданного пользователя в БД')

    def handle(self, *args, **options):
        total = options.get('total') or 1
        password = options.get('password') or '123'
        role = 'mediator' if options.get('mediator') else 'client'
        if options.get('email'):
            # небольшая валидация email
            mail = options.get('email').split('@')
            if len(mail) > 2:
                raise ValueError('Некорректный адрес электронной почты')
            elif len(mail) == 1:
                username, server = mail + ['mail.ru']
            elif len(mail) == 2:
                username, server = mail
        else:
            username, server = ('user' if role == 'client' else 'mediator'), 'mail.ru'

        if role == 'mediator':
            count = Mediator.objects.count() + 1
        else:
            count = BasicUser.objects.count() + 1

        for i in range(count, count + total):
            user = CreateUser()
            user.create(password=password, role=role, username=username, num=i, server=server)
