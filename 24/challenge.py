from abc import ABC, abstractmethod


class Challenge(ABC):
    def __init__(self, number, title):
        self.number = number
        self.title = title

    @abstractmethod
    def verify(self):
        return "Subclasses obj should verify"

    @abstractmethod
    def pretty_title(self):
        return "Subclasses obj should verify"


class BlogChallenge(Challenge):
    def __init__(self, number, title, merged_prs):
        super().__init__(number, title)
        self.merged_prs = merged_prs

    def verify(self, pr):
        return pr in self.merged_prs

    @property
    def pretty_title(self):
        return f"PCC{self.number} - {self.title}"


class BiteChallenge(Challenge):
    def __init__(self, number, title, result):
        super().__init__(number, title)
        self.result = result

    def verify(self, result):
        return result == self.result

    @property
    def pretty_title(self):
        return f"Bite {self.number}. ABC and class inheritance"


if __name__ == "__main__":
    blog = BlogChallenge(1, "Wordvalues", [41, 42, 44])
    print(blog.verify(43))
    print(blog.pretty_title)
