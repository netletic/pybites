import re


MIN_PASSWORD_LENGTH = 8


def password_complexity(password: str) -> int:
    """Input: password string, calculate score according to 5 criteria in bite,
    return: score int"""
    score = 0

    # password has both lower- and uppercase letters
    lower = re.compile(r"[a-z]+")
    upper = re.compile(r"[A-Z]+")
    has_lower_and_upper_letter = re.search(lower, password) and re.search(
        upper, password
    )
    score += 1 if has_lower_and_upper_letter else 0

    # password contains one or more numbers in addition to one or more characters
    number = re.compile(r"\d+")
    char = re.compile(r"\D+")
    has_number_and_char = re.search(number, password) and re.search(char, password)
    score += 1 if has_number_and_char else 0

    # password has one or more special characters
    special_char = re.compile(r"[^A-Za-z0-9]+")
    has_special_char = re.search(special_char, password)
    score += 1 if has_special_char else 0

    # password has a minimum length of MIN_PASSWORD_LENGTH characters
    has_min_length = len(password) >= MIN_PASSWORD_LENGTH
    score += 1 if has_min_length else 0

    # first MIN_PASSWORD_LENGTH chars don't repeat
    min_length_unique = all(
        [c != password[i] for i, c in enumerate(password[1:MIN_PASSWORD_LENGTH], 0)]
    )
    score += 1 if min_length_unique and has_min_length else 0

    return score
