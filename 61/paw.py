import random
from collections import namedtuple
from itertools import cycle, product
from string import ascii_uppercase
from typing import List

ACTIONS = ["draw_card", "play_again", "interchange_cards", "change_turn_direction"]
NUMBERS = range(1, 5)

PawCard = namedtuple("PawCard", "card action")


def _create_cards(n: int) -> List[str]:
    """Returns the cards that will make up the deck"""
    if n > 26:
        raise ValueError("n must be <= 26")
    letters = ascii_uppercase[:n]
    return [f"{letter}{number}" for letter, number in product(letters, NUMBERS)]


def _assign_action_cards(cards: List[str]) -> List[str]:
    """Returns a quarter of the cards that will get actions assigned to them"""
    return set(random.sample(cards, len(cards) // 4))


def create_paw_deck(n=8):
    cards = _create_cards(n)
    action_cards = _assign_action_cards(cards)
    possible_actions = cycle(ACTIONS)

    deck = []
    for card in cards:
        action = next(possible_actions) if card in action_cards else None
        deck.append(PawCard(card, action))
    return deck
