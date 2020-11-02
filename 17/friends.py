from itertools import combinations, permutations


def friends_teams(friends: tuple, team_size: int = 2, order_does_matter: bool = False):
    f = permutations if order_does_matter else combinations
    return f(friends, team_size)
