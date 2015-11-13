import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import os
from app import app


def test_text_content():
    test_app = app.test_client()
    content = '<h1>Great headline</h1>'
    # Create a content file
    with open('content/test_text_content.html', 'w') as f:
        f.write(content)

    # Create path file
    with open('templates/_test_text_content.html', 'w') as f:
        f.write("{{ text_content('test_text_content.html')|safe }}")

    data = test_app.get('/test_text_content').data.decode('utf8')
    assert content in data
    assert 'tinymce.init' not in data

    os.remove('templates/_test_text_content.html')
    os.remove('content/test_text_content.html')
