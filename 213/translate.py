import re


def fix_translation(org_text: str, trans_text: str) -> str:
    """Receives original English text as well as text returned by translator.
    Parse trans_text restoring the original (English) code (wrapped inside
    code and pre tags) into it. Return the fixed translation str
    """
    pattern = re.compile(r"<code>.+?<\/code>|<pre>.+?<\/pre>", re.DOTALL)
    correct = re.findall(pattern, org_text)
    wrong = re.findall(pattern, trans_text)
    for orig, trans in zip(correct, wrong):
        trans_text = trans_text.replace(trans, orig)
    return trans_text
