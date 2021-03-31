import re
from urllib.parse import urlparse


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:
    def __init__(self, name: str):
        valid_domain_name = re.match(r".*\.[a-z]{2,3}$", name)
        if valid_domain_name:
            self.name = name
        else:
            raise DomainException

    def __str__(self):
        return self.name

    @classmethod
    def parse_url(cls, url: str):
        domain_portion = urlparse(url).netloc
        return cls(name=domain_portion)

    @classmethod
    def parse_email(cls, email: str):
        _, _, domain_portion = email.partition("@")
        return cls(name=domain_portion)
