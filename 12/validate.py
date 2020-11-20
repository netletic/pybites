from collections import namedtuple

User = namedtuple("User", "name role expired")
USER, ADMIN = "user", "admin"
SECRET = "I am a very secret token"

julian = User(name="Julian", role=USER, expired=False)
bob = User(name="Bob", role=USER, expired=True)
pybites = User(name="PyBites", role=ADMIN, expired=False)
USERS = (julian, bob, pybites)


# define exception classes here
class UserDoesNotExist(Exception):
    """User does not exist"""


class UserAccessExpired(Exception):
    """User access expired"""


class UserNoPermission(Exception):
    """User has no permission"""


# def _get_user(username):
#     users = {user.name: user for user in USERS}
#     return users.get(username)


def get_secret_token(username):
    # user = _get_user(username)
    # if not user:
    #     raise UserDoesNotExist
    try:
        user = next(user for user in USERS if user.name == username)
    except StopIteration:
        raise UserDoesNotExist

    if user.expired:
        raise UserAccessExpired

    if user.role != ADMIN:
        raise UserNoPermission

    return SECRET


print(get_secret_token("PyBites"))
