from functools import total_ordering


@total_ordering
class Account:
    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, position):
        return self._transactions[position]

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __add__(self, amount):
        if isinstance(amount, int):
            return self._transactions.append(amount)
        else:
            raise ValueError

    def __sub__(self, amount):
        if isinstance(amount, int):
            return self._transactions.append(-amount)
        else:
            raise ValueError

    def __str__(self):
        return f"{self.name} account - balance: {self.balance}"
