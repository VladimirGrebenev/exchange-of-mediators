from random import sample
from user.models import Mediator


def random_mediators(request):
    mediators = Mediator.objects.all()
    num_mediators = min(mediators.count(), 5)  # определяем количество записей или возьмем 5
    random_mediators_list = sample(list(mediators), num_mediators)  # выбираем случайные записи из модели
    return {'random_records': random_mediators_list}


