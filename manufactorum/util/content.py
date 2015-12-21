import os


def update_file(file_name, content):
    file_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(file_path, '../content/', file_name)

    with open(path, 'w') as f:
        f.write(content)
