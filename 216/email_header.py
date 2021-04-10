import re


def get_email_details(header: str) -> dict:
    """User re.search or re.match to capture the from, to, subject
    and date fields. Return the groupdict() of matching object, see:
    https://docs.python.org/3.7/library/re.html#re.Match.groupdict
    If not match, return None
    """
    pattern = re.compile(
        r"From:\s(?P<from>.*)\n"
        r"To:\s(?P<to>.*)\n"
        r"Subject:\s(?P<subject>.*?)\n.*\n*"
        r"Date:\s(?P<date>.*)\s[+-]"
    )
    if match := re.search(pattern, header):
        return match.groupdict()
