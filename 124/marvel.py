import csv
import heapq
import re
from collections import Counter, namedtuple

import requests

MARVEL_CSV = "https://raw.githubusercontent.com/pybites/marvel_challenge/master/marvel-wikia-data.csv"  # noqa E501

Character = namedtuple("Character", "pid name sid align sex appearances year")


# csv parsing code provided so this Bite can focus on the parsing


def _get_csv_data():
    """Download the marvel csv data and return its decoded content"""
    with requests.Session() as session:
        return session.get(MARVEL_CSV).content.decode("utf-8")


def load_data():
    """Converts marvel.csv into a sequence of Character namedtuples
    as defined above"""
    content = _get_csv_data()
    reader = csv.DictReader(content.splitlines(), delimiter=",")
    for row in reader:
        name = re.sub(r"(.*?)\(.*", r"\1", row["name"]).strip()
        appearances = int(row["APPEARANCES"]) if row["APPEARANCES"] else 0
        yield Character(
            pid=row["page_id"],
            name=name,
            sid=row["ID"],
            align=row["ALIGN"],
            sex=row["SEX"],
            appearances=appearances,
            year=row["Year"],
        )


characters = list(load_data())


# start coding


def most_popular_characters(characters=characters, top=5):
    """Get the most popular character by number of appearances,
    return top n characters (default 5)
    """
    ntop_chars = heapq.nlargest(top, characters, key=lambda char: char.appearances)
    return [char.name for char in ntop_chars]


def max_and_min_years_new_characters(characters=characters):
    """Get the year with most and least new characters introduced respectively,
    use either the 'FIRST APPEARANCE' or 'Year' column in the csv
    characters, or the 'year' attribute of the namedtuple, return a tuple
    of (max_year, min_year)
    """
    years = (char.year for char in characters if char.year)
    most, *_, least = Counter(years).most_common()
    return (most[0], least[0])


def get_percentage_female_characters(characters=characters):
    """Get the percentage of female characters as percentage of all genders
    over all appearances.
    Ignore characters that don't have gender ('sex' attribue) set
    (in your characters data set you should only have Male, Female,
    Agender and Genderfluid Characters.
    Return the result rounded to 2 digits
    """
    genders = Counter(char.sex for char in characters if char.sex)
    return round(genders["Female Characters"] / sum(genders.values()) * 100, 2)


if __name__ == "__main__":
    from pprint import pprint

    pprint(characters)
