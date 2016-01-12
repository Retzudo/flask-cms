import os
import hashlib
from manufactorum import cache
from flask import url_for

ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif'])
IMAGE_DIRECTORY = 'static/images'


def update_file(file_name, content):
    file_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(file_path, 'content/', file_name)

    with open(path, 'w') as f:
        f.write(content)

    cache.clear()


def save_file(file):
    if allowed_file(file.filename):
        sha = hashlib.sha1()
        content = file.read()
        sha.update(content)
        new_file_name = sha.hexdigest() + get_file_extension(file.filename)
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), IMAGE_DIRECTORY, new_file_name)

        with open(path, 'wb') as f:
            f.write(content)

        print(file)
        return os.path.join('/', IMAGE_DIRECTORY, new_file_name)


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


def allowed_file(filename):
    return '.' in filename and \
        get_file_extension(filename).lower() in ALLOWED_EXTENSIONS
