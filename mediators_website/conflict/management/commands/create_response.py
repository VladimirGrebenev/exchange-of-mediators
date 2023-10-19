from django.core.management.base import BaseCommand
from conflict.forms import ResponseForm
from user.models import Mediator
from conflict.models import Conflict
from faker import Faker
from random import choice
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class CreateResponse:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = {}
        conflicts = Conflict.objects.all()
        mediators = Mediator.objects.all()

        if not (conflicts and mediators):
            raise ValueError('В базе данных нет конфликтов или медиаторов')

        for c in conflicts:
            responded_mediators = [r.mediator.id for r in c.responses.all()]
            for m in Mediator.objects.exclude(id__in=responded_mediators):
                self.container[m] = c

    def get_random_data(self):
        mediator, conflict = choice(list(self.container.items()))
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

    def create(self):
        try:
            data = self.get_random_data()
            form = ResponseForm(data=data)
            if form.is_valid():
                form.save()
                print(f'Отклик на конфликт {data.get("conflict").title[:10]}... '
                      f'создан медиатором {data.get("mediator").lastname} {data.get("mediator").firstname}')
        except IndexError:
            pass


class Command(BaseCommand):
    help = """
        Создание откликов медиаторов на конфликты.
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых откликов')

    def handle(self, *args, **options):
        total = options.get('total') or 1

        for i in range(total):
            response = CreateResponse()
            response.create()
