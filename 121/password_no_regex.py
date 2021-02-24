MIN_LENGTH = 8


def _has_lower_upper(password):
    return any([c.islower() for c in password]) and any([c.isupper() for c in password])


def _has_number_and_char(password):
    return any([c.isdigit() for c in password]) and any([c.isalpha() for c in password])


def _has_special(password):
    return not password.isalnum()


def _is_long_enough(password):
    return len(password) >= MIN_LENGTH


def _is_long_enough_without_repetition(password):
    if not _is_long_enough(password):
        return False
    previous = ""
    for c in password:
        if c == previous:
            return False
        previous = c
    return True


def password_complexity(password):
    score = 0
    if _has_lower_upper(password):
        score += 1
    if _has_number_and_char(password):
        score += 1
    if _has_special(password):
        score += 1
    if _is_long_enough(password):
        score += 1
    if _is_long_enough_without_repetition(password):
        score += 1
    return score