import heapq
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Tuple

bites: List[int] = [283, 282, 281, 263, 255, 230, 216, 204, 197, 196, 195]
names: List[str] = [
    "snow",
    "natalia",
    "alex",
    "maquina",
    "maria",
    "tim",
    "kenneth",
    "fred",
    "james",
    "sara",
    "sam",
]


@dataclass(order=True)
class Ninja:
    """
    The Ninja class will have the following features:

    string: name
    integer: bites
    support <, >, and ==, based on bites
    print out in the following format: [469] bob
    """

    name: str = field(compare=False)
    bites: int

    def __str__(self) -> str:
        return f"[{self.bites}] {self.name}"


@dataclass
class Rankings:
    """
    The Rankings class will have the following features:

    method: add() that adds a Ninja object to the rankings
    method: dump() that removes/dumps the lowest ranking Ninja from Rankings
    method: highest() returns the highest ranking Ninja, but it takes an optional
            count parameter indicating how many of the highest ranking Ninjas to return
    method: lowest(), the same as highest but returns the lowest ranking Ninjas, also
            supports an optional count parameter
    returns how many Ninjas are in Rankings when len() is called on it
    method: pair_up(), pairs up study partners, takes an optional count
            parameter indicating how many Ninjas to pair up
    returns List containing tuples of the paired up Ninja objects
    """

    ranking: List[Ninja] = field(init=False, default_factory=list)

    def add(self, ninja: Ninja) -> None:
        heapq.heappush(self.ranking, ninja)

    def dump(self) -> Ninja:
        return heapq.heappop(self.ranking)

    def lowest(self, count: int = 1) -> List[Ninja]:
        return heapq.nsmallest(count, self.ranking)

    def highest(self, count: int = 1) -> List[Ninja]:
        return heapq.nlargest(count, self.ranking)

    def pair_up(self, count: int = 3) -> List[Tuple[Ninja, Ninja]]:
        return list(zip(self.highest(count), self.lowest(count)))

    def __len__(self) -> int:
        return len(self.ranking)
