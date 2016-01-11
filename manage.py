#!/usr/bin/env python3
import sys
import pytest
from flask.ext.script import Manager
from manufactorum import app
from manufactorum import users
from getpass import getpass

manager = Manager(app)


@manager.option(
    '-h', '--host',
    dest='host',
    default='127.0.0.1'
)
@manager.option(
    '-p', '--port',
    dest='port',
    default='5000'
)
@manager.option(
    '--no-debug',
    dest='no_debug',
    action='store_true',
    help='Disable debugging mode'
)
def run(host='127.0.0.1', port=5000, no_debug=False):
    app.run(host=host, port=int(port), debug=(not no_debug))


@manager.command
def add_admin():
    username = input('Username: ')
    password = getpass('Password: ')
    password_repeat = getpass('Repeat: ')

    if password == password_repeat:
        try:
            users.add_user(username, password)
            print('User {} added successfully'.format(username))
        except ValueError:
            print(
                'User {} already exists.'.format(username),
                file=sys.stderr
            )
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
