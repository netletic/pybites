LETTER_CASE_REGEX = re.compile(r"(?=.*[a-z])(?=.*[A-Z])")
DIGIT_LETTER_REGEX = re.compile(r"(?=.*[a-zA-Z])(?=.*[0-9])")
SPECIAL_CHAR_REGEX = re.compile(r"(?=.*\W)")
LENGTH_REGEX = re.compile(r".{8,}")
REPEATING_REGEX = re.compile(r"(.)\1")


def password_complexity(password):
    """Input: password string, calculate score according to 5 criteria in bite,
    return: score int"""
    score = 0

    if LETTER_CASE_REGEX.search(password):
        score += 1
    if DIGIT_LETTER_REGEX.search(password):
        score += 1
    if SPECIAL_CHAR_REGEX.search(password):
        score += 1
    if LENGTH_REGEX.search(password):
        score += 1
        if not REPEATING_REGEX.search(password):
            score += 1

    return score