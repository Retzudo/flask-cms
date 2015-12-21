import os
from manufactorum import app


def test_text_content():
    test_app = app.test_client()
    content = '<h1>Great headline</h1>'
    # Create a content file
    with open('manufactorum/content/test_text_content.html', 'w') as f:
        f.write(content)

    # Create path file
    with open('manufactorum/templates/_test_text_content.html', 'w') as f:
        f.write("{{ text_content('test_text_content.html')|safe }}")

    data = test_app.get('/test_text_content').data.decode('utf8')
    assert content in data
    assert 'tinymce.init' not in data

    os.remove('manufactorum/templates/_test_text_content.html')
    os.remove('manufactorum/content/test_text_content.html')
