scores = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
ranks = "white yellow orange green blue brown black paneled red".split()
BELTS = dict(zip(scores, ranks))


class NinjaBelt:
    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    @staticmethod
    def _get_belt(new_score):
        """Might be a useful helper"""
        for score in reversed(BELTS):
            if new_score >= score:
                return BELTS[score]

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):
        try:
            new_score = int(new_score)
        except ValueError:
            raise ValueError("Score takes an int")
        if new_score < self.score:
            raise ValueError("Cannot lower score")

        self._score = new_score
        belt_is_new = self._last_earned_belt != self._get_belt(self.score)
        if belt_is_new:
            self._last_earned_belt = self._get_belt(self._score)
            print(
                f"Congrats, you earned {self._score} points obtaining the PyBites Ninja {self._last_earned_belt.capitalize()} Belt"  # noqa E501
            )
        else:
            print(f"Set new score to {self._score}")


if __name__ == "__main__":
    nj = NinjaBelt(10)
    print(nj._last_earned_belt)
    nj.score = 20
    print(nj._last_earned_belt)
