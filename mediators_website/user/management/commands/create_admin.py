from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from signing.forms import UserRegisterForm
from user.models import User, Mediator, BasicUser
from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class CreateAdmin:
    def create(self, password, role, username, server):
        try:
            admin = User.objects.get(is_superuser=1)
        except User.DoesNotExist:
            pass
        else:
            admin.delete()


        firstname, lastname = 'Админ', 'Администратов'
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'password1': password,
            'password2': password,
            'role': role,
            'email': f'{username}@{server}',
        }
        form = UserRegisterForm(data=data)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.is_superuser = True
            admin.is_staff = True
            new_group, _ = Group.objects.get_or_create(name='user')
            admin.groups.set([new_group])
            admin.save()
            print(f'Создан admin: Email: {admin.email}')


class Command(BaseCommand):
    help = """
        Создание администратора
    """

    def add_arguments(self, parser):
        parser.add_argument('-p', '--password', type=str, help='Пароль для user. По умолчанию пароль "123"')
        parser.add_argument('-e', '--email', type=str, help='Указать email')

    def handle(self, *args, **options):
        password = options.get('password') or '123'
        role = 'client'
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
            username, server = 'admin', 'mail.ru'

        admin = CreateAdmin()
        admin.create(password=password, role=role, username=username, server=server)
