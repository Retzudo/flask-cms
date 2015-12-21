import pytest
import os
import manufactorum.util.users as users
from manufactorum.util.users import User
from unittest.mock import patch
from tests.unittest_utils import temp_file


def test_user_class():
    user = User('User')
    assert user.username == 'User'
    assert user.get_id() == 'User'
    assert user.password_hash is None

    same_username_user = User('User', 'other invalid hash')
    assert user == same_username_user
    assert same_username_user.password_hash == 'other invalid hash'

    assert user.__str__() == 'User'
    assert user.__repr__() == "<class 'manufactorum.util.users.User'> 'User'"


def test_user_password():
    user = User('This is me')
    assert user.check_password('badpassword') is False

    user.set_password('badpassword')
    assert '$rounds=' in user.password_hash

    assert user.check_password('badpassword') is True
    assert user.check_password('wrongpassword') is False


def test_load_users():
    with temp_file('testusers.dat'):
        with patch('manufactorum.util.users.USERS_FILE', 'testusers.dat'):
            assert users.load_users() == []

            users.add_user(
                'test_load_users_user',
                'test_load_users_user_password'
            )

            assert len(users.load_users()) == 1
            assert users.user_exists('test_load_users_user') is True
            assert users.user_exists('Someone') is False

            user = users.get_user('test_load_users_user')
            assert user is not None
            assert user.username == 'test_load_users_user'
            assert user.check_password('test_load_users_user_password') is True

            users.remove_user('test_load_users_user')


def test_add_user():
    test_file = 'test_users.tmp'
    try:
        os.remove(test_file)
    except FileNotFoundError:
        pass

    with patch('manufactorum.util.users.USERS_FILE', test_file):
        users.add_user('user', 'user')
        user = users.get_user('user')

        assert user is not None
        assert user.username == 'user'
        assert user.check_password('user') is True

        with pytest.raises(Exception):
            users.add_user('user', 'user')

        os.remove(test_file)


def test_remove_user():
    user = users.add_user(
        'test_remove_user_user',
        'test_remove_user_user_password'
    )
    assert user is not None
    assert user.username == 'test_remove_user_user'
    assert user.check_password('test_remove_user_user_password') is True

    users.remove_user('test_remove_user_user')
    assert users.get_user('test_remove_user_user') is None
