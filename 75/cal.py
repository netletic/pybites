from itertools import chain
from itertools import cycle
from itertools import repeat

WEEKDAYS = "Su Mo Tu We Th Fr Sa".split()


def pad_none(iterable):
    """Returns the sequence elements and then returns None indefinitely."""
    return chain(iterable, repeat(None))


def line_contains_int_days(line: str):
    return all([item.isdigit() for item in line.split()])


def get_int_days(line: str):
    return [int(number) for number in line.split()]


def get_weekdays(calendar_output: str):
    """Receives a multiline Unix cal output and returns a mapping (dict) where
    keys are int days and values are the 2 letter weekdays (Su Mo Tu ...)"""
    cal = {}
    for line in calendar_output.splitlines():
        if not line_contains_int_days(line):
            continue
        f = reversed if line[1] == " " else lambda x: x
        days = get_int_days(line)
        weekday_cycle = cycle(f(WEEKDAYS))
        for day in f(days):
            cal[day] = next(weekday_cycle)
    return cal


if __name__ == "__main__":
    cal = """    January 1986
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
"""
    print(get_weekdays(cal))
