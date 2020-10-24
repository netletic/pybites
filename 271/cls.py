import csv
import inspect


def get_classes(mod):
    """Return a list of all classes in module 'mod'"""
    return [
        member
        for member, _ in inspect.getmembers(mod, inspect.isclass)
        if member[0].isupper()
    ]


if __name__ == "__main__":
    print(get_classes(csv))
