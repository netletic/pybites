from datetime import datetime, date, timedelta
import re

TODAY = date(2018, 11, 12)


def extract_dates(data):
    """Extract unique dates from DB table representation as shown in Bite"""
    uniq_date_strings = set(re.findall(r"\d{4}-\d{2}-\d{2}", data))
    dates = [datetime.strptime(dt, "%Y-%m-%d").date() for dt in uniq_date_strings]
    return sorted(dates)


def calculate_streak(dates):
    """Receives sequence (set) of dates and returns number of days
    on coding streak.

    Note that a coding streak is defined as consecutive days coded
    since yesterday, because today is not over yet, however if today
    was coded, it counts too of course.

    So as today is 12th of Nov, having dates 11th/10th/9th of Nov in
    the table makes for a 3 days coding streak.

    See the tests for more examples that will be used to pass your code.
    """
    streak = 0

    for i in range(1, len(dates) + 1):
        if TODAY - timedelta(days=i) in dates:
            streak += 1
        else:
            break

    if TODAY in dates:
        streak += 1

    return streak


if __name__ == "__main__":
    data = """
    +------------+------------+---------+
    | date       | activity   | count   |
    |------------+------------+---------|
    | 2018-11-10 | pcc        | 1       |
    | 2018-11-09 | 100d       | 1       |
    | 2018-11-07 | 100d       | 2       |
    | 2018-10-23 | pcc        | 1       |
    | 2018-10-15 | pcc        | 1       |
    | 2018-10-05 | bite       | 1       |
    | 2018-09-21 | bite       | 4       |
    | 2018-09-18 | bite       | 2       |
    | 2018-09-18 | bite       | 4       |
    +------------+------------+---------+
    """
    from pprint import pprint

    dates = extract_dates(data)
    longest_streak = calculate_streak(dates)
    print(longest_streak)
