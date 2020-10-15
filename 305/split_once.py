from random import sample
from string import ascii_letters, whitespace
from typing import List


def split_once(text: str, separators: str = None) -> List[str]:
    seps = separators or whitespace
    uniq_sep = "".join([c for c in sample(ascii_letters, 32) if c not in seps])

    for sep in seps:
        text = text.replace(sep, uniq_sep, 1)

    return text.split(uniq_sep)


print(split_once("abc: def: ijk, lmno: pqr - stu, wxy", separators=",-:"))
