import re


def count_n_repetitions(text, n=1):
    """
    Counts how often characters are followed by themselves for
    n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    """
    count = 0
    for i, char in enumerate(text, start=0):
        if re.match(rf"{re.escape(char)}(?={re.escape(char)}{{{n}}})", text[i:]):
            count += 1
    return count


def count_n_reps_or_n_chars_following(text, n=1, char=""):
    """
    Counts how often characters are repeated for n times, or
    followed by char n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    char: Character which also counts if repeated n times
    """
    if char == "":
        return count_n_repetitions(text, n)

    count = 0
    for i, c in enumerate(text, start=0):
        pattern_c = re.compile(rf"{re.escape(c)}(?={re.escape(c)}{{{n}}})")
        pattern_char = re.compile(rf"{re.escape(c)}(?={re.escape(char)}{{{n}}})")
        if re.match(pattern_c, text[i:]):
            count += 1
            continue
        if re.match(pattern_char, text[i:]):
            count += 1
    return count


def check_surrounding_chars(text, surrounding_chars):
    """
    Count the number of times a character is surrounded by
    characters from the surrounding_chars list.

    text: UTF-8 compliant input text
    surrounding_chars: List of characters
    """
    escaped_surround_chars = re.escape("".join(surrounding_chars))
    surround_pattern = "[" + escaped_surround_chars + "]"

    hits = re.findall(
        rf"""
        (?<=    # start look-behind group
                {surround_pattern}
        )       # end look-behind group
        (.)     # match all characters
        (?=     # start look-ahead group
                {surround_pattern}
        )       # end look-ahead group
        """,
        text,
        flags=re.DOTALL | re.VERBOSE,
    )

    return len(hits)


def main() -> int:
    pass


if __name__ == "__main__":
    print(check_surrounding_chars("ABCCBAAAZz", ["Z", "A"]))
    exit(main())
