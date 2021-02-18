from random import choice


defeated_by = dict(paper="scissors", rock="paper", scissors="rock")
CHOICES = list(defeated_by.keys())
lose = "{} beats {}, you lose!"
win = "{} beats {}, you win!"
tie = "tie!"


def _get_computer_move():
    """Randomly select a move"""
    return choice(CHOICES)


def _get_winner(computer_choice, player_choice):
    """Return above lose/win/tie strings populated with the
    appropriate values (computer vs player)"""
    invalid = player_choice not in CHOICES
    if invalid:
        return "Invalid"

    if computer_choice == player_choice:
        return tie

    player_loses = defeated_by[player_choice] == computer_choice
    if player_loses:
        return lose.format(computer_choice, player_choice)

    player_wins = defeated_by[computer_choice] == player_choice
    if player_wins:
        return win.format(player_choice, computer_choice)


def game():
    """Game loop, receive player's choice via the generator's
    send method and get a random move from computer (_get_computer_move).
    Raise a StopIteration exception if user value received = 'q'.
    Check who wins with _get_winner and print its return output."""
    print("Welcome to Rock Paper Scissors")
    while True:
        player_choice = yield
        computer_choice = _get_computer_move()

        if player_choice == "q":
            raise StopIteration

        outcome = _get_winner(computer_choice, player_choice)
        print(outcome)


if __name__ == "__main__":
    g = game()
    next(g)
    g.send("paper")