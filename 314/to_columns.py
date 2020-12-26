from functools import partial
from itertools import islice
from typing import List


def take(n, iterable):
    """Return first *n* items of the iterable as a list."""
    return list(islice(iterable, n))


def chunked(iterable, n):
    """Break *iterable* into lists of length *n*"""
    return iter(partial(take, n, iter(iterable)), [])


def print_names_to_columns(names: List[str], cols: int = 2) -> None:
    rows = chunked(names, cols)
    result = []
    for row in rows:
        string = ""
        for name in row:
            string += f"| {name:<10}"
        result.append(string)
    print("\n".join(list(result)))


if __name__ == "__main__":
    names = "Sara Tim Ana Julian"
    print(print_names_to_columns(names.split(), cols=4))
