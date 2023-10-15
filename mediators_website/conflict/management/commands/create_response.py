from django.core.management.base import BaseCommand
from conflict.forms import ResponseForm
from user.models import Mediator
from conflict.models import Conflict
from faker import Faker
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class Command(BaseCommand):
    help = """
        Создание откликов на конфликты.
            -t, --total     Количество создаваемых откликов
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых откликов')

    def get_random_data(self):
        try:
            conflict = fake.random_choices(elements=Conflict.objects.all(), length=1)[0]
            mediator = fake.random_choices(elements=Mediator.objects.all(), length=1)[0]
        except IndexError:
            raise ValueError('В базе нет конфликтов или медиаторов. Выполни команды: "python manage.py create_conflict" или "python manage.py create_user -m"')
        rate = fake.random_number(digits=4)
        time_for_conflict = fake.random_number(digits=1)
        comment = fake.text(150)

        return {
            'conflict': conflict,
            'mediator': mediator,
            'rate': rate,
            'time_for_conflict': time_for_conflict,
            'comment': comment,
        }

    def handle(self, *args, **options):
        total = options.get('total') or 1

        for i in range(total):
            data = self.get_random_data()
            form = ResponseForm(data=data)
            if form.is_valid():
                form.save()
                print(f'Отклик на конфликт {data.get("conflict").title[:10]}... создан медиатором {data.get("mediator").firstname}')
            else:
                print(form.errors)
