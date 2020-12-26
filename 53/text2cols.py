from itertools import zip_longest
from textwrap import wrap, fill

COL_WIDTH = 20


def text_to_columns(text: str):
    """Split text (input arg) to columns, the amount of double
    newlines (\n\n) in text determines the amount of columns.
    Return a string with the column output like:
    line1\nline2\nline3\n ... etc ...
    See also the tests for more info."""
    paragraphs = (line.strip() for line in text.split("\n\n"))
    wrapped = (wrap(p, width=COL_WIDTH) for p in paragraphs)
    lines = ("\t".join(line) for line in zip_longest(*wrapped, fillvalue=""))
    return "\n".join(lines)


if __name__ == "__main__":
    text = """My house is small but cosy."""
    print(text_to_columns(text))

    text = """My house is small but cosy.

    It has a white kitchen and an empty fridge."""
    print(text_to_columns(text))
