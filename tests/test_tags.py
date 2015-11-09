import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
#
# from util.tags import custom_tags
# from unittest.mock import patch
# from unittest.mock import mock_open
#
#
# @patch('util.tags.current_user')
# def test_text_content_tag(patched_flask_user):
#     patched_flask_user.is_authenticated = False
#
#     text_content = custom_tags().get('text_content')
#
#     content = '<h1>Great headline</h1>'
#
#     m = mock_open(read_data=content)
#     with patch('builtins.open', m):
#         assert content == text_content('file.html')
import os
from unittest.mock import patch
from app import app


def test_text_content():
    test_app = app.test_client()
    content = '<h1>Great headline</h1>'
    # Create a content file
    with open('content/unittest.html', 'w') as f:
        f.write(content)

    # Create path file
    with open('templates/_unittest.html', 'w') as f:
        f.write("{{ text_content('unittest.html')|safe }}")

    data = test_app.get('/unittest').data.decode('utf8')
    assert content in data
    assert 'tinymce.init' not in data

    os.remove('templates/_unittest.html')
    os.remove('content/unittest.html')


def test_text_content_logged_in():
    test_app = app.test_client()

    with patch('util.tags.is_logged_in', True):
        test_text_content()

        data = test_app.get('/unittest').data.decode('utf8')
        assert 'tinymce.init' in data
