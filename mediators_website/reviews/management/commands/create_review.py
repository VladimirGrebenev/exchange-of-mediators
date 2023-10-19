from django.core.management.base import BaseCommand
from reviews.forms import ReviewForm
from user.models import BasicUser, Mediator
from faker import Faker
from random import randint, choice
import logging


logging.getLogger('faker.factory').setLevel(logging.ERROR)

fake = Faker('ru-Ru')


class CreateReview:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = {}
        mediators = Mediator.objects.all()
        users = BasicUser.objects.all()

        if not (mediators and users):
            raise ValueError('В базе данных нет медиаторов или клиентов')

        for m in mediators:
            previous_reviewers = [r.from_user.id for r in m.reviews.all()]
            for u in BasicUser.objects.exclude(id__in=previous_reviewers):
                self.container[u] = m

    def get_random_data(self, symbols):
        user, mediator = choice(list(self.container.items()))
        rating = randint(1, 5)
        text = fake.text(symbols)

        return {
            'to_user': mediator,
            'from_user': user,
            'rating': rating,
            'text': text,
        }

    def create(self, symbols):
        try:
            data = self.get_random_data(symbols=symbols)
            form = ReviewForm(data=data)
            if form.is_valid():
                form.save()
                print(f'Отзыв написан пользователем {data.get("from_user").lastname} {data.get("from_user").firstname} '
                      f'на медиатора {data.get("to_user").lastname} {data.get("to_user").firstname}')
        except IndexError:
            pass


class Command(BaseCommand):
    help = """
        Создание отзывов о медиаторах.
    """

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, help=u'Количество создаваемых отзывов. По умолчанию 1')
        parser.add_argument('-s', '--symbols', type=int, help=u'Количество символов текста отзыва. По умолчанию 150')

    def handle(self, *args, **options):
        total = options.get('total') or 1
        symbols = options.get('symbols') or 150

        if total > Mediator.objects.count() * BasicUser.objects.count():
            total = Mediator.objects.count() * BasicUser.objects.count() or 1

        for i in range(total):
            review = CreateReview()
            review.create(symbols)

