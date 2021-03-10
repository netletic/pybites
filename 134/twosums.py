from itertools import combinations
from pprint import pprint


def two_sums(numbers, target):
    """Finds the indexes of the two numbers that add up to target.

    :param numbers: list - random unique numbers
    :param target: int - sum of two values from numbers list
    :return: tuple - (index1, index2) or None
    """
    sorted_numbers = sorted(numbers)
    pairs = combinations(sorted_numbers, 2)
    for n1, n2 in pairs:
        if n1 + n2 == target:
            return numbers.index(n1), numbers.index(n2)
    return None


if __name__ == "__main__":
    numbers = [3, 10, 14, 8, 15, 5, 16, 13, 9, 2]
    print(two_sums(numbers, 30))