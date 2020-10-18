from collections import Counter

import bs4
import requests

COMMON_DOMAINS = "https://bites-data.s3.us-east-2.amazonaws.com/" "common-domains.html"
TARGET_DIV = {"class": "middle_info_noborder"}


def get_common_domains(url=COMMON_DOMAINS):
    """Scrape the url return the 100 most common domain names"""
    with requests.session() as s:
        html = s.get(url).content.decode("utf-8")
    soup = bs4.BeautifulSoup(html, "html.parser")
    div = soup.find("div", TARGET_DIV)
    table = div.find("table")
    tds = table.find_all("td")
    domains = []
    for td in tds:
        if "%" in td.get_text() or td.find("img"):
            continue
        else:
            try:
                int(td.get_text())
            except ValueError:
                domains.append(td.get_text())
    return domains


def get_most_common_domains(emails, common_domains=None):
    """Given a list of emails return the most common domain names,
    ignoring the list (or set) of common_domains"""
    if common_domains is None:
        common_domains = get_common_domains()
    emails = [
        email.split("@")[1]
        for email in emails
        if email.split("@")[1] not in common_domains
    ]
    return Counter(emails).most_common()


print(
    get_most_common_domains(
        [
            "a@hotmail.com",
            "b@hotmail.se",
            "c@paris.com",
            "d@paris.com",
            "e@hotmail.it",
        ]
    )
)
