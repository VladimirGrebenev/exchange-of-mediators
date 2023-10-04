from random import sample


def sample_queryset(model, k=1):
    """Выборка k случайных неповторяющихся объектов"""
    k = min(k, model.objects.count())
    return sample(list(model.objects.all()), k=k)
