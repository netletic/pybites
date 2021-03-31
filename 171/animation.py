from itertools import cycle
from time import monotonic
from time import sleep

SPINNER_STATES = ["-", "\\", "|", "/"]  # had to escape \
STATE_TRANSITION_TIME = 0.1


def spinner(seconds):
    """Make a terminal loader/spinner animation using the imports above.
    Takes seconds argument = time for the spinner to run.
    Does not return anything, only prints to stdout."""
    spinner = cycle(SPINNER_STATES)
    stop_time = monotonic() + seconds
    while monotonic() < stop_time:
        print(f"\r{next(spinner)}", end="", flush=True)
        sleep(STATE_TRANSITION_TIME)


if __name__ == "__main__":
    spinner(2)
