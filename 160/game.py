import csv
import os
from collections import defaultdict
from urllib.request import urlretrieve


TMP = os.getenv("TMP", "/tmp")
DATA = "battle-table.csv"
BATTLE_DATA = os.path.join(TMP, DATA)
if not os.path.isfile(BATTLE_DATA):
    urlretrieve(f"https://bites-data.s3.us-east-2.amazonaws.com/{DATA}", BATTLE_DATA)


def _create_defeat_mapping():
    """Parse battle-table.csv building up a defeat_mapping dict
    with keys = attackers / values = who they defeat.
    """
    with open(BATTLE_DATA) as fp:
        csvreader = csv.DictReader(fp.readlines())
    defeat_mapping = defaultdict(set)
    for row in csvreader:
        attacker = row["Attacker"]
        for opponent, outcome in row.items():
            if outcome == "win":
                defeat_mapping[attacker].add(opponent)
    return defeat_mapping


def get_winner(player1, player2, defeat_mapping=None):
    """Given player1 and player2 determine game output returning the
    appropriate string:
    Tie
    Player1
    Player2
    (where Player1 and Player2 are the names passed in)

    Raise a ValueError if invalid player strings are passed in.
    """
    defeat_mapping = defeat_mapping or _create_defeat_mapping()

    if player1 not in defeat_mapping or player2 not in defeat_mapping:
        raise ValueError("invalid string")

    if player1 == player2:
        return "Tie"

    defeated_by_player1 = player2 in defeat_mapping[player1]
    return player1 if defeated_by_player1 else player2


if __name__ == "__main__":
    print(_create_defeat_mapping())
