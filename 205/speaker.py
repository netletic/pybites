from collections import Counter
from operator import concat
from functools import reduce
from itertools import chain
from pathlib import Path
from urllib.request import urlretrieve

import gender_guesser.detector as gender
from bs4 import BeautifulSoup as Soup

TMP = Path("/tmp")
PYCON_HTML = TMP / "pycon2019.html"
PYCON_PAGE = "https://bites-data.s3.us-east-2.amazonaws.com/pycon2019.html"

if not PYCON_HTML.exists():
    urlretrieve(PYCON_PAGE, PYCON_HTML)


def _get_soup(html=PYCON_HTML):
    return Soup(html.read_text(encoding="utf-8"), "html.parser")


def get_pycon_speaker_first_names(soup=_get_soup()):
    """Parse the PYCON_HTML using BeautifulSoup, extracting all
    speakers (class "speaker"). Note that some items contain
    multiple speakers so you need to extract them.
    Return a list of first names
    """
    speakers = (
        speaker.get_text().strip().replace(" /", ",").split(", ")
        for speaker in soup.find_all("span", attrs={"class": "speaker"})
    )
    # speakers_flat = reduce(concat, speakers)
    speakers_flat = chain.from_iterable(speakers)
    first_names = [speaker.split()[0] for speaker in speakers_flat]
    return first_names


def get_percentage_of_female_speakers(first_names):
    """Run gender_guesser on the names returning a percentage
    of female speakers (female and mostly_female),
    rounded to 2 decimal places."""
    g = gender.Detector()
    cnt = Counter((g.get_gender(name) for name in first_names))
    total = sum(cnt.values())
    females = cnt.get("female") + cnt.get("mostly_female")
    return round(females / total * 100, 2)


if __name__ == "__main__":
    names = get_pycon_speaker_first_names(_get_soup())
    perc = get_percentage_of_female_speakers(names)
    print(perc)
