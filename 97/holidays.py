from collections import defaultdict
import os
from urllib.request import urlretrieve

from bs4 import BeautifulSoup


# prep data
tmp = os.getenv("TMP", "/tmp")
page = "us_holidays.html"
holidays_page = os.path.join(tmp, page)
urlretrieve(f"https://bites-data.s3.us-east-2.amazonaws.com/{page}", holidays_page)

with open(holidays_page) as f:
    content = f.read()

holidays = defaultdict(list)


def get_us_bank_holidays(content=content):
    """Receive scraped html output, make a BS object, parse the bank
    holiday table (css class = list-table), and return a dict of
    keys -> months and values -> list of bank holidays"""
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", attrs="list-table")
    for tr in table.find_all("tr")[1:]:
        time = tr.find("time")
        href = tr.find("a")

        yy, mm, dd = time.get_text().split("-")
        day = href.get_text().strip()

        holidays[mm].append(day)

    return holidays
