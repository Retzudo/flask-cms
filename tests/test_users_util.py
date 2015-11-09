import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import pytest
import util.users
from util.users import User
from unittest.mock import patch
from unittest.mock import mock_open


def test_user_class():
    user = User('User')
    assert user.username == 'User'
    assert user.get_id() == 'User'
    assert user.password_hash is None

    same_username_user = User('User', 'other invalid hash')
    assert user == same_username_user
    assert same_username_user.password_hash == 'other invalid hash'

    assert user.__str__() == 'User'
    assert user.__repr__() == "<class 'util.users.User'> 'User'"


def test_user_password():
    user = User('This is me')
    assert user.check_password('badpassword') is False

    user.set_password('badpassword')
    assert '$rounds=' in user.password_hash

    assert user.check_password('badpassword') is True
    assert user.check_password('wrongpassword') is False


def test_load_users():
    m = mock_open()
    with patch('builtins.open', m):
        assert util.users.load_users() == []

    # Username: admin, password: admin
    f = 'admin:$5$rounds=535000$z0v1bgIQg9vv2bOF$oa4gjeEs1ktRJUCMyKKUcicWz43sS7Idxo8e3YZtI86'
    m = mock_open(read_data=f)
    with patch('builtins.open', m):
        assert len(util.users.load_users()) == 1
        assert util.users.user_exists('admin') is True
        assert util.users.user_exists('Someone') is False

        user = util.users.get_user('admin')
        assert user is not None
        assert user.username == 'admin'
        assert user.check_password('admin') is True


def test_add_user():
    test_file = 'test_users.tmp'
    try:
        os.remove(test_file)
    except FileNotFoundError:
        pass

    with patch('util.users.USERS_FILE', test_file):
        util.users.add_user('user', 'user')
        user = util.users.get_user('user')

        assert user is not None
        assert user.username == 'user'
        assert user.check_password('user') is True

        with pytest.raises(Exception):
            util.users.add_user('user', 'user')

        os.remove(test_file)
