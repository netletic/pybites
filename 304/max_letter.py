from typing import Tuple
from collections import Counter
from string import digits, punctuation


def only_count(text: str) -> str:
    new_text = ""
    do_not_count = str(digits) + punctuation + "-"
    for c in text.casefold():
        if c not in do_not_count:
            new_text += c
    return new_text


def _remove_random_crap(text: str) -> str:
    new_text = ""

    for c in text:
        if c not in digits and c not in u"\U0001F603":
            new_text += c
    return new_text


def _clean_word(text: str) -> str:
    clean_text = ""
    for c in text:
        if c in "-'" or c.isalpha():
            clean_text += c
    return clean_text


def max_letter_word(text: str) -> Tuple[str, str, int]:
    """
    Find the word in text with the most repeated letters. If more than one word
    has the highest number of repeated letters choose the first one. Return a
    tuple of the word, the (first) repeated letter and the count of that letter
    in the word.
    >>> max_letter_word('I have just returned from a visit...')
    ('returned', 'r', 2)
    >>> max_letter_word('$5000 !!')
    ('', '', 0)
    """
    if not isinstance(text, str):
        raise ValueError
    text = _remove_random_crap(text)
    words = text.split()
    char_count = []
    for word in words:
        try:
            char, count = Counter(only_count(word)).most_common(1)[0]
            char_count.append((_clean_word(word), char, count))
        except IndexError:
            pass
    return max(char_count, key=lambda x: x[2]) if char_count else ("", "", 0)


if __name__ == "__main__":
    sample_text = "1, 2, 3"
    print(max_letter_word(sample_text))
