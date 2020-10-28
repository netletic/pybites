from typing import Dict


def decompress(string: str, table: Dict[str, str]) -> str:
    if not string:
        return string

    trans_table = str.maketrans(table)

    while set(table) & set(string):
        string = string.translate(trans_table)
    return string


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
