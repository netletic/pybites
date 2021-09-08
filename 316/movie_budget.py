from collections import defaultdict
from datetime import date
from typing import Dict
from typing import NamedTuple
from typing import Sequence


class MovieRented(NamedTuple):
    title: str
    price: int
    date: date


RentingHistory = Sequence[MovieRented]
STREAMING_COST_PER_MONTH = 12
STREAM, RENT = "stream", "rent"


def rent_or_stream(
    renting_history: RentingHistory,
    streaming_cost_per_month: int = STREAMING_COST_PER_MONTH,
) -> Dict[str, str]:
    """Function that calculates if renting movies one by one is
    cheaper than streaming movies by months.

    Determine this PER MONTH for the movies in renting_history.

    Return a dict of:
    keys = months (YYYY-MM)
    values = 'rent' or 'stream' based on what is cheaper

    Check out the tests for examples.
    """
    rented = defaultdict(list)
    for movie_rented in renting_history:
        rented[f"{movie_rented.date.year}-{movie_rented.date.month}"].append(
            movie_rented.price
        )

    total_rented = {
        dt: "stream" if sum(prices) > streaming_cost_per_month else "rent"
        for dt, prices in rented.items()
    }

    return total_rented
