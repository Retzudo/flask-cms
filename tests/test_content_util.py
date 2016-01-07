from manufactorum import content
import os


def test_update_file():
    filename = 'some_file.html'
    text = """
        This is some test content.
        <h1>Great headline man!</h1>
    """
    content.update_file(filename, text)

    with open('manufactorum/content/{}'.format(filename)) as f:
        assert text == f.read()

    os.remove('manufactorum/content/{}'.format(filename))
