from typing import List


def sum_indices(items: List[str]) -> int:
    values = []
    seen = {}
    for i, string in enumerate(items):
        if string not in seen:
            value = i
            seen[string] = i
        else:
            value = seen.get(string) + i
            seen[string] = value
        values.append(value)
    return sum(values)


if __name__ == "__main__":
    print(sum_indices(["a", "b", "b", "c", "a", "b", "a"]))
