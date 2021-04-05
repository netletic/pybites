from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from itertools import cycle
from os import getenv
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup  # type: ignore

TMP = getenv("TMP", "/tmp")
TODAY = date.today()

CANDIDATES = ["Biden", "Sanders", "Gabbard"]


class Candidate(NamedTuple):
    name: str
    votes: str


class LeaderBoard(NamedTuple):
    Candidate: str
    Average: str
    Delegates: int
    Contributions: str
    Coverage: int


class Poll(NamedTuple):
    Poll: str
    Date: str
    Sample: str
    Sanders: float
    Biden: float
    Gabbard: float
    Spread: str


@dataclass
class File:
    """File represents a filesystem path.

    Variables:
        name: str -- The filename that will be created on the filesystem.
        path: Path -- Path object created from the name passed in.

    Methods:
        [property]
        data: -> Optional[str] -- If the file exists, it returns its contents.
            If it does not exist, it returns None.
    """

    name: str

    def __post_init__(self):
        self.path = Path(TMP, f"{TODAY}_{self.name}")

    @property
    def data(self) -> Optional[str]:
        try:
            return self.path.read_text()
        except FileNotFoundError:
            return None


@dataclass
class Web:
    """Web object.

    Web is an object that downloads the page from the url that is passed
    to it and stores it in the File instance that is passed to it. If the
    File already exists, it just reads the file, otherwise it downloads it
    and stores it in File.

    Variables:
        url: str -- The url of the web page.
        file: File -- The File object to store the page data into.

    Methods:
        [property]
        data: -> Optional[str] -- Reads the text from File or retrieves it from the
            web if it does not exists.

        [property]
        soup: -> Soup -- Parses the data from File and turns it into a Soup
            object.
    """

    url: str
    file: File

    @property
    def data(self) -> Optional[str]:
        """Reads the data from the File object.

        First it checks if the File object has any data. If it doesn't, it retrieves
        it and saves it to the File. It then reads it from the File and returns it.

        Returns:
            Optional[str] -- The string data from the File object.
        """
        content = self.file.data
        if content is not None:
            return content
        try:
            urlretrieve(self.url, self.file.path)
        except (ValueError, HTTPError, URLError) as exc:
            raise exc
        else:
            return self.file.data

    @property
    def soup(self) -> Soup:
        """Converts string data from File into a Soup object.

        Returns:
            Soup -- Soup object created from the File.
        """
        soup = Soup(self.data, "html.parser")
        return soup


class Site(ABC):
    """Site Abstract Base Class.

    Defines the structure for the objects based on this class and defines the interfaces
    that should be implemented in order to work properly.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        [abstractmethod]
        parse_rows: -> Union[List[LeaderBoard], List[Poll]] -- Parses a Soup
            table element and returns the text found in the td elements as
            namedtuples.

        [abstractmethod]
        polls: -> Union[List[LeaderBoard], List[Poll]] -- Does the parsing of the table
            and rows for you. It takes the table index number if given, otherwise
            parses table 0.

        [abstractmethod]
        stats: -- Formats the results from polls into a more user friendly
            representation.
    """

    web: Web

    def find_table(self, loc: int = 0) -> str:
        """Finds the table elements from the Soup object

        Keyword Arguments:
            loc {int} -- Parses the Web object for table elements and
                returns the first one that it finds unless an integer representing
                the required table is passed. (default: {0})

        Returns:
            str -- The html table
        """
        return self.web.soup.find_all("table")[loc]

    @abstractmethod
    def parse_rows(self, table: Soup) -> List[Any]:
        """Abstract Method

        Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a Soup table element and
                returns the text found in the td elements as NamedTuple.

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def polls(self, table: int = 0) -> List[Any]:
        """Abstract Method

        Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def stats(self, loc: int = 0):
        """Abstract Method

        Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        pass


@dataclass
class RealClearPolitics(Site):
    """RealClearPolitics object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[Poll] -- Parses a Soup table element and
            returns the text found in the td elements as Poll namedtuples.

        polls: -> List[Poll] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            RealClearPolitics
            =================
                Biden: 214.0
              Sanders: 142.0
              Gabbard: 6.0

    """

    web: Web

    def parse_rows(self, table: Soup) -> List[Poll]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a Soup table element and
                returns the text found in the td elements as Poll namedtuples.

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """

        polls = []
        rows = table("tr")
        candidate_cycle = cycle(CANDIDATES)
        for row in rows[2:]:
            pollster, dt, sample, *votes, spread = row.find_all("td")
            dt = dt.get_text()
            sample = sample.get_text()
            pollster = pollster.get_text()
            spread = spread.get_text()
            count: Dict[str, float] = defaultdict(float)
            for vote in votes:
                try:
                    count[next(candidate_cycle)] += float(vote.get_text())
                except ValueError:
                    continue
            poll = Poll(
                Poll=pollster,
                Date=dt,
                Sample=sample,
                Sanders=count.get("Sanders", 0.0),
                Biden=count.get("Biden", 0.0),
                Gabbard=count.get("Gabbard", 0.0),
                Spread=spread,
            )
            polls.append(poll)
        return polls

    def polls(self, table: int = 0) -> List[Poll]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """
        return self.parse_rows(self.find_table(table))

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.

        """
        polls = self.polls(loc)
        biden = sum(poll.Biden for poll in polls)
        sanders = sum(poll.Sanders for poll in polls)
        gabbard = sum(poll.Gabbard for poll in polls)
        name = self.__class__.__name__
        results = f"\n{name}\n"
        results += f"{'=' * len(name)}\n"
        results += f"{'Biden:':>8} {biden}\n"
        results += f"{'Sanders:':>8} {sanders}\n"
        results += f"{'Gabbard:':>8} {gabbard}\n"
        print(results)
        return 0


@dataclass
class NYTimes(Site):
    """NYTimes object.

    NYTimes is a custom class to parse a Web instance from the nytimes website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[LeaderBoard] -- Parses a Soup table element and
            returns the text found in the td elements as LeaderBoard namedtuples.

        polls: -> List[LeaderBoard] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            NYTimes
            =================================

                               Pete Buttigieg
            ---------------------------------
            National Polling Average: 10%
                   Pledged Delegates: 25
            Individual Contributions: $76.2m
                Weekly News Coverage: 3

    """

    web: Web

    def parse_rows(self, table: Soup) -> List[LeaderBoard]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a Soup table element and
                returns the text found in the td elements as LeaderBoard namedtuples.

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
            the table data.
        """
        """
        class Candidate(NamedTuple):
            name: str
            votes: int


        class LeaderBoard(NamedTuple):
            Candidate: Candidate
            Average: float
            Delegates: int
            Contributions: float
            Coverage: int
        """
        table_rows = table.find("tbody")("tr")
        boards = []
        for row in table_rows[:3]:

            table_data = row("td")
            name = table_data[0].find("span", {"class": "g-desktop"}).get_text()
            avg = table_data[1].find("span", {"class": "g-contents"}).get_text()
            deleg = int(table_data[2].find("span", {"class": "g-contents"}).get_text())
            contrib = table_data[3].find("span", {"class": "g-contents"}).get_text()
            cov = int(
                table_data[4]
                .find("span", {"class": "g-contents"})
                .get_text()
                .lstrip("#")
            )
            board = LeaderBoard(
                Candidate=name,
                Average=avg,
                Delegates=deleg,
                Contributions=contrib,
                Coverage=cov,
            )
            boards.append(board)
        return boards

    def polls(self, table: int = 0) -> List[LeaderBoard]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
                the table data.
        """
        return self.parse_rows(self.find_table(loc=table))

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        spacing = 33
        boards = self.polls(table=loc)
        print(f"\n{self.__class__.__name__}\n")
        print("=" * spacing)
        for board in boards:
            print(f"\n{board.Candidate.rjust(spacing)}")
            print("-" * spacing)
            print(f"{'National Polling Average:':>{spacing-8}} {board.Average}")
            print(f"{'Pledged Delegates:':>{spacing-8}} {board.Delegates}")
            print(f"{'Individual Contributions:':>{spacing-8}} {board.Contributions}")
            print(f"{'Weekly News Coverage:':>{spacing-8}} {board.Coverage}")


def gather_data():
    rcp_file = File("realclearpolitics.html")
    rcp_url = "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_realclearpolitics.html"  # noqa
    rcp_web = Web(rcp_url, rcp_file)
    rcp = RealClearPolitics(rcp_web)
    rcp.stats(3)

    nyt_file = File("nytimes.html")
    nyt_url = "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_nytimes.html"
    nyt_web = Web(nyt_url, nyt_file)
    nyt = NYTimes(nyt_web)
    nyt.stats()


if __name__ == "__main__":
    gather_data()
