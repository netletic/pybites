import json
import os
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

import pytest

from zodiac import (
    Sign,
    _get_month_int,
    get_sign_by_date,
    get_sign_with_most_famous_people,
    get_signs,
    signs_are_mutually_compatible,
)

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "zodiac.json")


@pytest.fixture(scope="module")
def signs():
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH) as f:
        data = json.loads(f.read())
    return get_signs(data)


# write your pytest code here ...
def test_get_signs_returns_list_of_signs(signs):
    assert type(signs) == list
    assert len(signs) == 12
    assert isinstance(signs[0], Sign)
    assert isinstance(signs[-1], Sign)


def test_get_signs_class_name_is_signs(signs):
    assert repr(signs[0]).startswith("Sign")


def test_sign_with_most_famous_people(signs):
    actual = get_sign_with_most_famous_people(signs)
    expected = ("Scorpio", 35)
    assert actual == expected


def test_signs_mutually_compatible(signs):
    assert signs_are_mutually_compatible(signs, "Gemini", "Libra")
    assert signs_are_mutually_compatible(signs, "Libra", "Gemini")

    assert not signs_are_mutually_compatible(signs, "Gemini", "Scorpio")
    assert not signs_are_mutually_compatible(signs, "Scorpio", "Gemini")


@pytest.mark.parametrize("month, expected", [("January", 1), ("Decenber", 12)])
def test_get_month_int(month, expected):
    assert _get_month_int(month) == expected


def test_get_sign_by_date_aries(signs):
    assert get_sign_by_date(signs, datetime(2021, 3, 21)) == "Aries"
    assert get_sign_by_date(signs, datetime(2021, 4, 19)) == "Aries"


def test_get_sign_by_date_taurus(signs):
    assert get_sign_by_date(signs, datetime(2021, 4, 20)) == "Taurus"
    assert get_sign_by_date(signs, datetime(2021, 5, 20)) == "Taurus"


def test_get_sign_by_date_gemini(signs):
    assert get_sign_by_date(signs, datetime(2021, 5, 21)) == "Gemini"
    assert get_sign_by_date(signs, datetime(2021, 6, 20)) == "Gemini"


def test_get_sign_by_date_cancer(signs):
    assert get_sign_by_date(signs, datetime(2021, 6, 22)) == "Cancer"
    assert get_sign_by_date(signs, datetime(2021, 7, 22)) == "Cancer"


def test_get_sign_by_date_leo(signs):
    assert get_sign_by_date(signs, datetime(2021, 7, 23)) == "Leo"
    assert get_sign_by_date(signs, datetime(2021, 8, 22)) == "Leo"


def test_get_sign_by_date_virgo(signs):
    assert get_sign_by_date(signs, datetime(2021, 8, 23)) == "Virgo"
    assert get_sign_by_date(signs, datetime(2021, 9, 22)) == "Virgo"


def test_get_sign_by_date_libra(signs):
    assert get_sign_by_date(signs, datetime(2021, 9, 23)) == "Libra"
    assert get_sign_by_date(signs, datetime(2021, 10, 22)) == "Libra"


def test_get_sign_by_date_scorpio(signs):
    assert get_sign_by_date(signs, datetime(2021, 10, 23)) == "Scorpio"
    assert get_sign_by_date(signs, datetime(2021, 11, 21)) == "Scorpio"


def test_get_sign_by_date_sagittarius(signs):
    assert get_sign_by_date(signs, datetime(2021, 11, 22)) == "Sagittarius"
    assert get_sign_by_date(signs, datetime(2021, 12, 21)) == "Sagittarius"


def test_get_sign_by_date_capricorn(signs):
    assert get_sign_by_date(signs, datetime(2021, 12, 22)) == "Capricorn"
    assert get_sign_by_date(signs, datetime(2021, 1, 19)) == "Capricorn"


def test_get_sign_by_date_aquarius(signs):
    assert get_sign_by_date(signs, datetime(2021, 1, 20)) == "Aquarius"
    assert get_sign_by_date(signs, datetime(2021, 2, 18)) == "Aquarius"


def test_get_sign_by_date_pisces(signs):
    assert get_sign_by_date(signs, datetime(2021, 2, 19)) == "Pisces"
    assert get_sign_by_date(signs, datetime(2021, 3, 20)) == "Pisces"


# or do
@pytest.mark.parametrize(
    "month, day, expected",
    [
        (3, 21, "Aries"),
        (4, 19, "Aries"),
        (4, 20, "Taurus"),
        (5, 1, "Taurus"),
        (5, 20, "Taurus"),
        (5, 21, "Gemini"),
        (6, 20, "Gemini"),
        (6, 21, "Cancer"),
        (7, 1, "Cancer"),
        (7, 22, "Cancer"),
        (8, 22, "Leo"),
        (8, 23, "Virgo"),
        (9, 1, "Virgo"),
        (9, 22, "Virgo"),
        (9, 23, "Libra"),
        (10, 22, "Libra"),
        (10, 23, "Scorpio"),
        (11, 21, "Scorpio"),
        (11, 22, "Sagittarius"),
        (12, 1, "Sagittarius"),
        (12, 21, "Sagittarius"),
        (12, 22, "Capricorn"),
        (1, 19, "Capricorn"),
        (1, 20, "Aquarius"),
        (2, 18, "Aquarius"),
        (2, 19, "Pisces"),
        (3, 1, "Pisces"),
        (3, 20, "Pisces"),
    ],
)
def test_get_sign_by_date(signs, month, day, expected):
    actual = get_sign_by_date(signs, datetime(year=2021, month=month, day=day))
    assert actual == expected
