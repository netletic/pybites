from collections import namedtuple
from operator import itemgetter

import requests
from bs4 import BeautifulSoup

Question = namedtuple("Question", "question views votes")
MIN_VIEWS = 1000000

cached_so_url = "https://bites-data.s3.us-east-2.amazonaws.com/so_python.html"


def top_python_questions(url=cached_so_url):
    """Use requests to retrieve the url / html,
    parse the questions out of the html with BeautifulSoup,
    filter them by >= 1m views ("..m views").
    Return a list of (question, num_votes) tuples ordered
    by num_votes descending (see tests for expected output).
    """
    with requests.Session() as session:
        html = session.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    questions = soup.select(".question-summary")
    res = []

    for que in questions:
        question = que.select_one(".question-hyperlink").get_text()
        votes = que.select_one(".vote-count-post").get_text()
        views = que.select_one(".views").get_text().strip()

        if "m views" not in views:
            continue

        res.append((question, int(votes)))

    return sorted(res, key=itemgetter(1), reverse=True)
