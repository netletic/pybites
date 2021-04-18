from unittest.mock import patch

import pytest

from guess import GuessGame, InvalidNumber

# write test code to reach 100% coverage and a 100% mutpy score


def test_not_a_number_raises_invalid_number_exception():
    with pytest.raises(InvalidNumber) as exc:
        GuessGame("a")
    assert "Not a number" in str(exc.value)


def test_negative_number_raises_invalid_number_exception():
    with pytest.raises(InvalidNumber) as exc:
        GuessGame("-1")
    assert "Negative number" in str(exc.value)


def test_number_gt_max_number_raises_invalid_number_exception():
    with pytest.raises(InvalidNumber) as exc:
        GuessGame("16")
    assert "Number too high" in str(exc.value)


def test_valid_guess_game_constructor_default_max_guesses():
    g = GuessGame(15)
    assert g.max_guesses == 5
    assert g.attempt == 0
    assert g.secret_number == 15

    g = GuessGame(0)
    assert g.max_guesses == 5
    assert g.attempt == 0
    assert g.secret_number == 0


def test_valid_guess_game_constructor_custom_max_guesses():
    g = GuessGame(secret_number=10, max_guesses=3)
    assert g.max_guesses == 3
    assert g.attempt == 0
    assert g.secret_number == 10


def test_max_guesses_exceeded(capfd):
    g = GuessGame(secret_number=10, max_guesses=0)
    assert g.attempt == 0
    g()
    assert g.attempt == 0
    output = capfd.readouterr()[0].strip()
    assert output == "Sorry, the number was 10"


@patch("builtins.input", side_effect=[9, 11])
def test_game_lose(inp, capfd):
    g = GuessGame(secret_number=10, max_guesses=2)
    g()

    out, _ = capfd.readouterr()
    expected = [
        "Guess a number:",
        "Too low",
        "Guess a number:",
        "Too high",
        "Sorry, the number was 10",
    ]
    output = [line.strip() for line in out.split("\n") if line.strip()]
    for line, exp in zip(output, expected):
        assert line == exp
    assert g.attempt == g.max_guesses


@patch("builtins.input", side_effect=[10])
def test_game_win(inp, capfd):
    g = GuessGame(secret_number=10, max_guesses=1)
    g()

    out, _ = capfd.readouterr()
    expected = [
        "Guess a number:",
        "You guessed it!",
    ]
    assert "You guessed it" in out
    output = [line.strip() for line in out.split("\n") if line.strip()]
    for line, exp in zip(output, expected):
        assert line == exp
    assert g.attempt == g.max_guesses


@patch("builtins.input", side_effect=["a", "%", 10])
def test_game_not_a_number(inp, capfd):
    g = GuessGame(secret_number=10, max_guesses=2)
    g()

    out, _ = capfd.readouterr()
    expected = [
        "Guess a number:",
        "Enter a number, try again",
        "Guess a number:",
        "Enter a number, try again",
        "Guess a number:",
        "You guessed it!",
    ]
    output = [line.strip() for line in out.split("\n") if line.strip()]
    for line, exp in zip(output, expected):
        assert line == exp
    assert g.attempt == 1
