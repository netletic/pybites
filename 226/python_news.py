from collections import namedtuple

from bs4 import BeautifulSoup
import requests

# feed = https://news.python.sc/, to get predictable results we cached
# first two pages - use these:
url1 = "https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html"
url2 = "https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index2.html"

Entry = namedtuple("Entry", "title points comments")


def _create_soup_obj(url):
    """Need utf-8 to properly parse emojis"""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def get_top_titles(url, top=5):
    """Parse the titles (class 'title') using the soup object.
    Return a list of top (default = 5) titles ordered descending
    by number of points and comments.
    """
    soup = _create_soup_obj(url)

    span_title = soup.find_all("span", attrs={"class": "title"})
    titles = [item.get_text().strip() for item in span_title]

    span_smaller = soup.find_all("span", attrs={"class": "controls"})
    points = [int(item.get_text().split(" point")[0].strip()) for item in span_smaller]
    comments = [
        int(item.get_text().split("|")[-1].strip().rstrip(" comments"))
        for item in span_smaller
    ]

    entries = []
    for t, p, c in zip(titles, points, comments):
        entries.append(Entry(t, p, c))

    return sorted(
        entries, key=lambda entry: (entry.points, entry.comments), reverse=True
    )[:top]


from pprint import pprint

pprint(
    get_top_titles(
        "https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html"
    )
)
# pprint(get_top_titles(url2))
