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
    assert util.users.load_users() == []

    util.users.add_user(
        'test_load_users_user',
        'test_load_users_user_password'
    )

    assert len(util.users.load_users()) == 1
    assert util.users.user_exists('test_load_users_user') is True
    assert util.users.user_exists('Someone') is False

    user = util.users.get_user('test_load_users_user')
    assert user is not None
    assert user.username == 'test_load_users_user'
    assert user.check_password('test_load_users_user_password') is True

    util.users.remove_user('test_load_users_user')


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


def test_remove_user():
    user = util.users.add_user(
        'test_remove_user_user',
        'test_remove_user_user_password'
    )
    assert user is not None
    assert user.username == 'test_remove_user_user'
    assert user.check_password('test_remove_user_user_password') is True

    util.users.remove_user('test_remove_user_user')
    assert util.users.get_user('test_remove_user_user') is None
