from typing import List


def jagged_list(lst_of_lst: List[List[int]], fillvalue: int = 0) -> List[List[int]]:
    max_length = len(max(lst_of_lst, key=len)) if lst_of_lst else 0
    for lst in lst_of_lst:
        if len(lst) != max_length:
            while len(lst) < max_length:
                lst.append(fillvalue)
    return lst_of_lst


if __name__ == "__main__":
    print(
        jagged_list(
            [
                [1, 2, 3],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [1, 2],
                [1, 2, 3, 4],
            ]
        )
    )
