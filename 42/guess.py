import random

MAX_GUESSES = 5
START, END = 1, 20


def get_random_number():
    """Get a random number between START and END, returns int"""
    # return 6
    return random.randint(START, END)


class Game:
    """Number guess class, make it callable to initiate game"""

    def __init__(self):
        """Init _guesses, _answer, _win to set(), get_random_number(), False"""
        self._answer = get_random_number()
        self._guesses = set()
        self._win = False

    def guess(self):
        """Ask user for input, convert to int, raise ValueError outputting
        the following errors when applicable:
        'Please enter a number'
        'Should be a number'
        'Number not in range'
        'Already guessed'
        If all good, return the int"""
        number = input(f"Guess a number between {START} and {END}: ")

        if not number:
            raise ValueError("Please enter a number")

        number = number.strip('"') if isinstance(number, str) else number

        try:
            number = int(number)
        except ValueError:
            raise ValueError("Should be a number")

        if number < START or number > END:
            raise ValueError("Number not in range")
        # if number in self._guesses:
        #     raise ValueError("Already guessed")

        return number

    def _validate_guess(self, guess):
        """Verify if guess is correct, print the following when applicable:
        {guess} is correct!
        {guess} is too low
        {guess} is too high
        Return a boolean"""
        if guess == self._answer:
            print(f"{guess} is correct!")
            return True
        else:
            reply = "low" if guess < self._answer else "high"
            print(f"{guess} is too {reply}")
            return False

    def __call__(self):
        """Entry point / game loop, use a loop break/continue,
        see the tests for the exact win/lose messaging"""
        while len(self._guesses) < MAX_GUESSES:
            try:
                number = self.guess()
                len_guesses = len(self._guesses)
                self._guesses.add(number)
                if len_guesses == len(self._guesses):
                    raise ValueError
                    raise ValueError("Already guessed")
                if self._validate_guess(number):
                    self._win = True
                    break
            except ValueError as ve:
                print(ve)
                continue
        if self._win:
            print(f"It took you {len(self._guesses)} guesses")
        else:
            print(f"Guessed {len(self._guesses)} times, answer was {self._answer}")


if __name__ == "__main__":
    game = Game()
    game()