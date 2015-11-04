def update_file(filename, content):
    with open('content/{}'.format(filename), 'w') as f:
        f.write(content)
