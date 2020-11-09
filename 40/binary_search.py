def binary_search(sequence, target):
    sequence = sorted(sequence)

    left = 0
    right = len(sequence)

    while left <= right:
        middle = (left + right) // 2
        if sequence[middle] < target:
            left = middle + 1
        elif sequence[middle] > target:
            right = middle - 1
        else:
            return middle
    return None


if __name__ == "__main__":
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    res = binary_search(PRIMES, 59)
    print(res)