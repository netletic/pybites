from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from urllib.request import urlretrieve

from bs4 import BeautifulSoup
from bs4 import Tag

url = "https://bites-data.s3.us-east-2.amazonaws.com/best-programming-books.html"
tmp = Path("/tmp")
html_file = tmp / "books.html"

if not html_file.exists():
    urlretrieve(url, html_file)


@dataclass
class Book:
    """Book class should instantiate the following variables:

    title - as it appears on the page
    author - should be entered as lastname, firstname
    year - four digit integer year that the book was published
    rank - integer rank to be updated once the books have been sorted
    rating - float as indicated on the page
    """

    title: str
    author: str
    year: int
    rank: int
    rating: float

    @property
    def last_name(self) -> str:
        last_name, _, _ = self.author.partition(",")
        return last_name

    @property
    def ranking(self) -> str:
        return str(self.rank).zfill(3)

    @property
    def ordering(self) -> Tuple[float, int, str, str]:
        return (
            -self.rating,
            self.year,
            self.title.lower(),
            self.last_name,
        )

    def __str__(self):
        result = ""
        result += f"[{self.ranking}] {self.title} ({self.year})\n"
        result += f"      {self.author} {float(self.rating)}"
        return result


def _get_soup(file):
    return BeautifulSoup(file.read_text(), "html.parser")


def display_books(
    books: List[Book], limit: Optional[int] = 10, year: Optional[int] = None
) -> None:
    """Prints the specified books to the console

    :param books: list of all the books
    :param limit: integer that indicates how many books to return
    :param year: integer indicating the oldest year to include
    :return: None
    """
    books = [book for book in books if book.year >= year] if year else books
    for book in books[:limit]:
        print(book)


def parse_row(row: Tag) -> Optional[Book]:
    try:
        title = row.select_one("h2.main").text
        if "python" not in title.lower():
            return None

        author_string = row.select_one("h3.authors > a").text
        first, _, last = author_string.rpartition(" ")
        author = f"{last}, {first}"

        year_string = row.select_one("span.date").text
        year = "".join(c for c in year_string if c.isdigit())

        rating = row.select_one("span.our-rating").text
    except AttributeError:
        return None
    else:
        return Book(title, author, int(year), 0, float(rating))


def load_data() -> List[Book]:
    """Loads the data from the html file

    Creates the soup object and processes it to extract the information
    required to create the Book class objects and returns a sorted list
    of Book objects.

    Books should be sorted by rating, year, title, and then by author's
    last name. After the books have been sorted, the rank of each book
    should be updated to indicate this new sorting order.The Book object
    with the highest rating should be first and go down from there.
    """
    soup = _get_soup(html_file)
    rows = soup("div", {"class": "book accepted normal"})

    books = []
    for row in rows:
        if book := parse_row(row):
            books.append(book)
    sorted_books = sorted(books, key=lambda x: x.ordering)

    updated_ranks = []
    for rank, book in enumerate(sorted_books, start=1):
        book.rank = rank
        updated_ranks.append(book)

    return updated_ranks


def main() -> int:
    books = load_data()
    display_books(books, limit=5, year=2017)
    return 0


if __name__ == "__main__":
    exit(main())
