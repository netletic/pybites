from unittest.mock import patch

import pytest

import color


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


@patch.object(color, "sample", side_effect=[[191, 165, 216], [101, 102, 103]])
def test_gen_hex_color(mock, gen):
    assert next(gen) == "#BFA5D8"
    assert next(gen) == "#656667"
