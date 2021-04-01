import re


def strip_single_line_comments(code: str) -> str:
    return "\n".join(
        [line for line in code.splitlines() if not line.lstrip().startswith("#")]
    )


def strip_single_line_docstring(code: str) -> str:
    pattern = re.compile(r"[\"\']{3}.*?[\"\']{3}")
    return "\n".join(
        [line for line in code.splitlines() if not re.search(pattern, line)]
    )


def strip_multiline_docstring(code: str) -> str:
    pattern = re.compile(r"[\"\']{3}.*?[\"\']{3}\n\s*", re.DOTALL)
    return re.sub(pattern, "", code)


def strip_inline_comment(code: str) -> str:
    pattern = re.compile(r"\s{2}# .*")
    return re.sub(pattern, "", code)


def strip_comments(code: str) -> str:
    strip_comments_funcs = [
        strip_single_line_comments,
        strip_inline_comment,
        strip_single_line_docstring,
        strip_multiline_docstring,
    ]
    for f in strip_comments_funcs:
        code = f(code)
    return code
