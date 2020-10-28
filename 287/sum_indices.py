from typing import List


def sum_indices(items: List[str]) -> int:
    seen, total = {}, 0

    for idx, char in enumerate(items):
        seen[char] = idx + seen.get(char, 0)
        total += seen.get(char)

    return total


if __name__ == "__main__":
    print(sum_indices(["a", "b", "b", "c", "a", "b", "a"]))
