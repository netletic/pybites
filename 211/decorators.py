from functools import wraps
from typing import Callable

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    """ raised when MAX_RETRIES is exceeded """


def retry(func: Callable) -> Callable:
    """Complete this decorator, make sure
    you print the exception thrown"""

    @wraps(func)
    def inner(*args, **kwargs):
        for _ in range(MAX_RETRIES):
            try:
                result = func(*args, **kwargs)
            except BaseException as exc:
                print(exc)
            else:
                return result
        else:
            raise MaxRetriesException

    return inner
