import sys
from urllib.parse import urlparse


INTERNAL_LINKS = ("pybit.es", "codechalleng.es")


def _fqdn(url: str) -> str:
    return urlparse(url).netloc


def make_html_links():
    output = []
    for line in sys.stdin:
        no_http = "http" not in line or "https" not in line
        if no_http:
            continue
        try:
            url, name = line.split(",")
        except ValueError as ve:
            print(ve)
            continue
        else:
            url, name = url.strip(), name.strip()
            external = _fqdn(url) not in INTERNAL_LINKS
            if external:
                output.append(f'<a href="{url}" target="_blank">{name}</a>')
            else:
                output.append(f'<a href="{url}">{name}</a>')
    print("\n".join(output))


if __name__ == "__main__":
    make_html_links()
