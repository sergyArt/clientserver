import logging
from functools import wraps

logger = logging.getLogger('decorators')


def logger_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}: {request}')
        logger.debug(f' Функция {func.__name__} вызвана из logger_required')
        return func(request, *args, **kwargs)
    return wrapper
