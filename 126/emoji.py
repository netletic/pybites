import sys
import unicodedata


START_EMOJI_RANGE = 100000  # estimate
NOT_FOUND = "Not found"


def what_means_emoji(emoji):
    """Receives emoji and returns its meaning,
    in case of a TypeError return 'Not found'"""
    try:
        return unicodedata.name(emoji)
    except (TypeError, ValueError):
        return NOT_FOUND


def _make_emoji_mapping():
    """Helper to make a mapping of all possible emojis:
    - loop through range(START_EMOJI_RANGE, sys.maxunicode +1)
    - return dict with keys=emojis, values=names"""
    for codepoint in range(START_EMOJI_RANGE, sys.maxunicode + 1):
        emoji = chr(codepoint)
        name = what_means_emoji(emoji)
        if name != NOT_FOUND:
            yield emoji, name


def find_emoji(term):
    """Return emojis and their texts that match (case insensitive)
    term, print matches to console"""
    term = term.lower()

    emoji_mapping = _make_emoji_mapping()

    for emoji, name in emoji_mapping:
        if term in name.lower():
            print(name, emoji)
