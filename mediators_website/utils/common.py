from random import sample


def sample_queryset(model, k=1):
    """Выборка k случайных неповторяющихся объектов"""
    k = min(k, model.objects.count())
    return sample(list(model.objects.all()), k=k)


def pluralize_word(count: int, sing: str, plur: str, other: str) -> str:
    """
    Возвращает склонение слова в зависимости от числа count..

    Примеры использования:
    >>> pluralize_word(1, "предмет", "предмета", "предметов")
    'предмет'
    >>> pluralize_word(2, "предмет", "предмета", "предметов")
    'предмета'
    >>> pluralize_word(5, "предмет", "предмета", "предметов")
    'предметов'
    """
    count = abs(count)
    if 10 < count % 100 < 15:
        return other
    elif count % 10 == 1:
        return sing
    elif 1 < count % 10 < 5:
        return plur
    else:
        return other
