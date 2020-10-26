from ipaddress import IPv4Address, IPv6Address
from more_itertools import collapse
from typing import List


def collapse_and_strip(data) -> List[str]:
    return [elem.strip('"') for elem in collapse(data) if elem]


def is_valid_cidr(elem: str) -> bool:
    try:
        return int(elem) <= 128
    except ValueError:
        return False


def is_valid_ip_address(elem: str) -> bool:
    try:
        return bool(IPv4Address(elem) or IPv6Address(elem))
    except ValueError:
        return False


def extract_ipv4(data):
    """
    Given a nested list of data return a list of IPv4 address information that can be extracted
    """
    flat_data = collapse_and_strip(data)

    ip_addresses = [elem for elem in flat_data if is_valid_ip_address(elem)]
    prefixes = [elem for elem in flat_data if is_valid_cidr(elem)]

    return list(zip(ip_addresses, prefixes))
