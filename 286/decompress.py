from typing import Dict


def translate(table: dict, string: str) -> str:
    for original, replacement in table.items():
        string = string.replace(original, replacement)
    return string


def decompress(string: str, table: Dict[str, str]) -> str:
    if not string:
        return string

    while any([key in str(table.values()) for key in table.keys()]):
        table = {k: translate(table, v) for k, v in table.items()}

    return translate(table, string)


if __name__ == "__main__":
    table = {
        "#": "hem",
        "@": "T#",
        "$": "t#",
        "&": "$ as",
        "*": " do ",
        "%": " to",
        "^": " someone ",
        "~": "for ",
        "+": "~&",
    }
    print(
        decompress("@ as can*has%*+ can't. And^has% speak up + has no voices.", table)
    )
