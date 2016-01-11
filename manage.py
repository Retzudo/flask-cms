#!/usr/bin/env python3
import sys
import pytest
from flask.ext.script import Manager
from manufactorum import app
from manufactorum import users
from getpass import getpass

manager = Manager(app)


@manager.option(
    '--no-debug',
    dest='no_debug',
    action='store_true',
    help='Disable debugging mode'
)
def run(no_debug=False):
    app.run(debug=(not no_debug))


@manager.command
def add_admin():
    username = input('Username: ')
    password = getpass('Password: ')
    password_repeat = getpass('Repeat: ')

    if password == password_repeat:
        users.add_user(username, password)
    else:
        print('Passwords did not match.', file=sys.stderr)


@manager.option(
    '-c', '--coverage',
    action='store_true',
    help='Run with coverage'
)
def test(coverage):
    args = ['--ignore=env']
    if coverage:
        args.append('--cov=manufactorum')
        args.append('--cov-report=term-missing')
    pytest.main(args)


if __name__ == '__main__':
    manager.run()
