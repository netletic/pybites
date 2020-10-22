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
    q_div = soup.find_all("div", attrs={"class": "question-summary"})

    questions = []

    for q in q_div:
        question = q.find("a", attrs={"class": "question-hyperlink"}).get_text()
        views = q.find("div", attrs={"class": "views"})["title"]
        views = int(views.replace(",", "").rstrip(" views"))
        votes = int(q.find("span", attrs={"class": "vote-count-post"}).get_text())
        questions.append(Question(question, views, votes))

    return sorted(
        [(q.question, q.votes) for q in questions if q.views > MIN_VIEWS],
        key=itemgetter(1),
        reverse=True,
    )
