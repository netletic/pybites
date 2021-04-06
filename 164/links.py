import sys

INTERNAL_LINKS = ("pybit.es", "codechalleng.es")
LINK_HTML = '<a href="{href}"{external}>{name}</a>'


def make_html_links():
    for line in sys.stdin:
        line = line.strip()

        if "http" not in line:
            continue

        try:
            href, name = line.split(",")
        except ValueError:
            continue

        external = ' target="_blank"'
        if any(il in href for il in INTERNAL_LINKS):
            external = ""

        print(LINK_HTML.format(href=href.strip(), external=external, name=name.strip()))


if __name__ == "__main__":
    make_html_links()
