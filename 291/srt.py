from datetime import timedelta
from typing import List
from pprint import pprint

from itertools import zip_longest
from dataclasses import dataclass


text1 = """
1
00:00:00,498 --> 00:00:02,827
Beautiful is better than ugly.

2
00:00:02,827 --> 00:00:06,383
Explicit is better than implicit.

3
00:00:06,383 --> 00:00:09,427
Simple is better than complex.
"""


@dataclass
class Section:
    idx: int
    duration: timedelta
    caption: str

    def __post_init__(self):
        self.speed = self.duration / len(self.caption)


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def caption_duration_from_string(string: str) -> int:
    t1, t2 = string.replace(",", ":").split(" --> ")

    def astimedelta(t: str) -> timedelta:
        h, m, s, ms = [int(unit) for unit in t.split(":")]
        return timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)

    return astimedelta(t2) - astimedelta(t1)


def get_srt_section_ids(text: str) -> List[int]:
    """Parse a caption (srt) text passed in and return a
    list of section numbers ordered descending by
    highest speech speed
    (= ratio of "time past:characters spoken")

    e.g. this section:

    1
    00:00:00,000 --> 00:00:01,000
    let's code

    (10 chars in 1 second)

    has a higher ratio then:

    2
    00:00:00,000 --> 00:00:03,000
    code

    (4 chars in 3 seconds)

    You can ignore milliseconds for this exercise.
    """
    sections = []

    for section in grouper(text.strip().splitlines(), 4):
        idx, duration, caption = [sec.strip() for sec in section if sec]
        idx = int(idx)
        duration = caption_duration_from_string(duration)
        sections.append(Section(idx, duration, caption))

    return [section.idx for section in sorted(sections, key=lambda x: x.speed)]


if __name__ == "__main__":
    pprint(get_srt_section_ids(text1))
