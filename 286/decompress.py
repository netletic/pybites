from typing import Dict


def decompress(string: str, table: Dict[str, str]) -> str:
    for v in table.values():
        for char in v.split():
    for char in string:
        string = string.replace(char, table.get(char, char))
    return string


if __name__ == "__main__":
    table = {"$": "s", "%": "y", "/": "t"}
    print(decompress("P%Bi/e$", table))
    table = {'*': 'c',

             '#': '00',

             '$': '*y',

             }
