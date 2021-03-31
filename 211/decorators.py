from functools import wraps

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    """ MaxRestriesException """


def retry(func):
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
