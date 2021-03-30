from datetime import date
from typing import List

from dateutil.rrule import DAILY
from dateutil.rrule import rrule


def get_missing_dates(dates: List[date]):
    """Receives a range of dates and returns a sequence
    of missing datetime.date objects (no worries about order).

    You can assume that the first and last date of the
    range is always present (assumption made in tests).

    See the Bite description and tests for example outputs.
    """
    start, end = min(dates), max(dates)
    all_dates = {dt.date() for dt in rrule(freq=DAILY, dtstart=start, until=end)}
    missing_dates = all_dates.difference(dates)
    return missing_dates
