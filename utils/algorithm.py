from typing import Iterable, Callable, Any


def first(iter: Iterable, predicate: Callable[[Any], bool] = lambda x: True):
    for i in iter:
        if predicate(i):
            return i
