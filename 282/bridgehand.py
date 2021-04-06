from collections import defaultdict
from collections import namedtuple
from enum import Enum
from typing import Sequence

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points


class BridgeHand:
    def __init__(self, cards: Sequence[Card]):
        """
        Process and store the sequence of Card objects passed in input.
        Raise TypeError if not a sequence
        Raise ValueError if any element of the sequence is not an instance
        of Card, or if the number of elements is not 13
        """
        if not isinstance(cards, Sequence):
            raise TypeError("not a sequence")
        if len(cards) != 13:
            raise ValueError("hand must contain 13 cards")
        self.cards = cards

        # group by suit
        self.suits = defaultdict(list)
        for card in self.cards:
            if not isinstance(card, Card):
                raise ValueError("not a sequence of Cards")
            self.suits[card.suit].append(card.rank)

        # sort cards within each suit
        for suit in self.suits.values():
            suit.sort(key=lambda card: card.value)

    def __str__(self) -> str:
        """
        Return a string representing this hand, in the following format:
        "S:AK3 H:T987 D:KJ98 C:QJ"
        List the suits in SHDC order, and the cards within each suit in
        AKQJT..2 order.
        Separate the suit symbol from its cards with a colon, and
        the suits with a single space.
        Note that a "10" should be represented with a capital 'T'
        """
        out = ""
        for suit in sorted(self.suits, key=lambda suit: suit.value):
            out += f"{suit.name}:"
            for rank in self.suits[suit]:
                out += rank.name
            out += " "
        return out.strip()

    @property
    def hcp(self) -> int:
        """ Return the number of high card points contained in this hand """
        return sum(HCP.get(card.rank, 0) for card in self.cards)

    @property
    def doubletons(self) -> int:
        """ Return the number of doubletons contained in this hand """
        return sum(len(cards) == 2 for cards in self.suits.values())

    @property
    def singletons(self) -> int:
        """ Return the number of singletons contained in this hand """
        return sum(len(cards) == 1 for cards in self.suits.values())

    @property
    def voids(self) -> int:
        """Return the number of voids (missing suits) contained in
        this hand
        """
        return 4 - len(self.suits)

    @property
    def ssp(self) -> int:
        """Return the number of short suit points in this hand.
        Doubletons are worth one point, singletons two points,
        voids 3 points
        """
        counter = 0
        counter += SSP[2] * self.doubletons
        counter += SSP[1] * self.singletons
        counter += SSP[0] * self.voids
        return counter

    @property
    def total_points(self) -> int:
        """ Return the total points (hcp and ssp) contained in this hand """
        return self.hcp + self.ssp

    @property
    def ltc(self) -> int:
        """Return the losing trick count for this hand - see bite description
        for the procedure
        """
        losers = 0
        for cards in self.suits.values():
            top_3 = cards[:3]
            honors = "AKQ"[: len(top_3)]
            losers += sum(card.name not in honors for card in top_3)
        return losers
