import inspect
import csv
from inspect import isclass


def get_classes(mod):
    """Return a list of all classes in module 'mod'"""
    return [
        name
        for name, type_ in inspect.getmembers(mod)
        if isclass(type_)
        if name[0].isupper()
    ]


if __name__ == "__main__":
    print(get_classes(csv))
