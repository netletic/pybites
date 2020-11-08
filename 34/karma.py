from collections import namedtuple
from datetime import datetime

Transaction = namedtuple("Transaction", "giver points date")
# https://twitter.com/raymondh/status/953173419486359552
Transaction.__new__.__defaults__ = (datetime.now(),)


class User:
    def __init__(self, name):
        self.name = name
        self._transactions = []

    def __add__(self, transaction):
        self._transactions.append(transaction)

    def __str__(self):
        fan = "fans" if self.fans > 1 else "fan"
        return f"{self.name} has a karma of {self.karma} and {self.fans} {fan}"

    @property
    def karma(self):
        return sum(self.points)

    @property
    def points(self):
        return [transaction.points for transaction in self._transactions]

    @property
    def fans(self):
        return len({transaction.giver for transaction in self._transactions})


if __name__ == "__main__":
    bob = User("bob")
    tim = User("tim")
    alice = User("alice")

    transactions = [
        Transaction(giver=alice, points=1),
        Transaction(giver=bob, points=2),
        Transaction(giver=tim, points=3),
        Transaction(giver=tim, points=4),
        Transaction(giver=alice, points=2),
    ]

    bob + transactions[0]
    print(bob.karma)