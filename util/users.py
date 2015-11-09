"""User and password utils."""
from flask_login import UserMixin
from passlib.hash import sha256_crypt

USERS_FILE = 'users.dat'


class User(UserMixin):
    """User class."""
    def __init__(self, username, password_hash=None):
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = sha256_crypt.encrypt(password)

    def check_password(self, password):
        if self.password_hash:
            return sha256_crypt.verify(password, self.password_hash)
        else:
            return False

    def get_id(self):
        return self.username

    def __eq__(self, other):
        return self.username == other.username

    def __str__(self):
        return self.username

    def __repr__(self):
        return "{} '{}'".format(self.__class__, self.username)


def load_users():
    """Load all users from the users file."""
    users = []
    try:
        with open(USERS_FILE) as f:
            for line in f.readlines():
                username, password_hash = line.split(':')
                user = User(username, password_hash)
                users.append(user)
    except IOError:
        return []

    return users


def get_user(id):
    """Get a single users from the list of users."""
    users = [user for user in load_users() if user.username == id]
    return users[0] if users else None


def user_exists(username):
    """Check if the given username is already in the users file."""
    return get_user(username) is not None


def add_user(username, password):
    """Add a user to the users file."""
    if not user_exists(username):
        user = User(username)
        user.set_password(password)
        with open(USERS_FILE, 'a+') as f:
            f.write('{}:{}'.format(user.username, user.password_hash))
    else:
        raise Exception('Users already exists.')
