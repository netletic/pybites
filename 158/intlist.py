import statistics
from typing import List
from typing import Sequence


class IntList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def mean(self):
        return statistics.mean(self)

    @property
    def median(self):
        return statistics.median(self)

    def append(self, numbers):
        numbers = self._as_list_of_ints(numbers)
        super().append(*numbers)

    def __add__(self, numbers):
        numbers = self._as_list_of_ints(numbers)
        return super().__add__(numbers)

    __iadd__ = __add__

    @staticmethod
    def _as_list_of_ints(numbers) -> List[int]:
        numbers = numbers if isinstance(numbers, Sequence) else [numbers]
        try:
            return [int(number) for number in numbers]
        except ValueError:
            raise TypeError
