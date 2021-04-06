from typing import Any
from typing import Iterable
from typing import Set


def intersection(*args: Iterable) -> Set[Any]:
    iterables = [set(iterable) for iterable in args if iterable]
    return set.intersection(*iterables) if iterables else set()


if __name__ == "__main__":
    print(intersection({1, 2, 3}, {2, 3, 4}, {3, 4}))
