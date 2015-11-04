import getpass
import sys
from util import users


if __name__ == '__main__':
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    password_repeat = getpass.getpass('Repeat: ')

    if password == password_repeat:
        users.add_user(username, password)
        
    else:
        print('Passwords did not match.', file=sys.stderr)
