import re

TEXT_WITH_DOTS = """
We are looking forward attending the next Pycon in the U.S.A.
in 2020. Hope you do so too. There is no better Python networking
event than Pycon. Meet awesome people and get inspired. Btw this
dot (.) should not end this sentence, the next one should. Have fun!
"""  # contains 6 sentences


def get_sentences(text):
    """Return a list of sentences as extracted from the text passed in.
    A sentence starts with [A-Z] and ends with [.?!]"""
    sentences = re.findall(r"[A-Z].*?[!?.](?=\s[A-Z]|$)", text, re.DOTALL)
    return [sentence.replace("\n", " ") for sentence in sentences]


def main() -> int:
    print(get_sentences(TEXT_WITH_DOTS))


if __name__ == "__main__":
    exit(main())
