from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from datetime import date
from time import mktime
from time import struct_time
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

import feedparser

FEED = "https://bites-data.s3.us-east-2.amazonaws.com/all.rss.xml"


def _convert_struct_time_to_dt(stime: struct_time):
    """Convert a time.struct_time as returned by feedparser into a
    datetime.date object, so:
    time.struct_time(tm_year=2016, tm_mon=12, tm_mday=28, ...)
    -> date(2016, 12, 28)
    """
    epoch = mktime(stime)
    return date.fromtimestamp(epoch)


@dataclass(order=True)
class Entry:
    date: date
    title: str = field(compare=False)
    link: str = field(compare=False)
    tags: List[str] = field(compare=False)

    @staticmethod
    def from_feedparser(entry: dict):
        dt = _convert_struct_time_to_dt(entry.get("published_parsed"))
        title = entry.get("title")
        link = entry.get("link")
        tags = [tag.term.lower() for tag in entry.get("tags")]
        return Entry(date=dt, title=title, link=link, tags=tags)

    def __hash__(self):
        return hash((self.date, self.title))

    def __str__(self):
        return f"{self.date.isoformat()} | {self.title} \t\t\t | {self.link}"


@dataclass
class EntrySearcher:
    entries: List[Entry]

    def __post_init__(self):
        self._tags: Dict[str, Set[Entry]] = defaultdict(set)
        for entry in self.entries:
            for tag in entry.tags:
                self._tags[tag.lower()].add(entry)

    def _search_params(self, query: str) -> Tuple[str, List[str]]:
        """ """
        if "&" in query:
            params = [param.lower() for param in query.split("&")]
            operator = "&"
        elif "|" in query:
            params = [param.lower() for param in query.split("|")]
            operator = "|"
        else:
            params = [query.lower()]
            operator = None
        return (operator, params)

    def find(self, query: str):
        if not query:
            return None
        operator, params = self._search_params(query)
        if not operator:
            res = self._tags.get(params[0], [])
            return sorted(res)
        if operator == "|":
            res = []
            for tag in params:
                res.extend(list(self._tags.get(tag, [])))
            return sorted(set(res))
        if operator == "&":
            res = []
            for entry in self.entries:
                if all(entry in self._tags[tag] for tag in params):
                    res.append(entry)
            return sorted(res)


def get_feed_entries(feed: str = FEED):
    """Use feedparser to parse PyBites RSS feed.
    Return a list of Entry namedtuples (date = date, drop time part)
    """
    feed: feedparser.FeedParserDict = feedparser.parse(feed)
    entries = [Entry.from_feedparser(entry) for entry in feed.entries]
    return entries


def filter_entries_by_tag(search, entry):
    """Check if search matches any tags as stored in the Entry namedtuple
    (case insensitive, only whole, not partial string matches).
    Returns bool: True if match, False if not.
    Supported searches:
    1. If & in search do AND match,
       e.g. flask&api should match entries with both tags
    2. Elif | in search do an OR match,
       e.g. flask|django should match entries with either tag
    3. Else: match if search is in tags
    """
    searcher = EntrySearcher([entry])
    return bool(searcher.find(search))


def main() -> int:
    """Entry point to the program
    1. Call get_feed_entries and store them in entries
    2. Initiate an infinite loop
    3. Ask user for a search term:
       - if enter was hit (empty string), print 'Please provide a search term'
       - if 'q' was entered, print 'Bye' and exit/break the infinite loop
    4. Filter/match the entries (see filter_entries_by_tag docstring)
    5. Print the title of each match ordered by date ascending
    6. Secondly, print the number of matches: 'n entries matched'
       (use entry if only 1 match)
    """
    entries = get_feed_entries()
    searcher = EntrySearcher(entries)
    while True:
        inp = input("Search for (q for exit): ")
        inp = inp.strip()
        if not inp:
            print("Please provide a search term\n")
            continue
        if inp == "q":
            print("Bye")
            break
        res = searcher.find(inp)
        for entry in res:
            print(entry)
        ent = "entry" if len(res) == 1 else "entries"
        print(f'\n{len(res)} {ent} matched "{inp}"\n')


if __name__ == "__main__":
    main()
