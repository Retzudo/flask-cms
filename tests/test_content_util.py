import sys
import os.path
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from util import content


def test_update_file():
    filename = 'some_file.html'
    text = """
        This is some test content.
        <h1>Great headline man!</h1>
    """
    content.update_file(filename, text)

    with open('content/{}'.format(filename)) as f:
        assert text == f.read()

    os.remove('content/{}'.format(filename))
