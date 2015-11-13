import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import app
from unittest_utils import temp_file

app.app.config.update(TESTING=True)
app.app.config.update(WTF_CSRF_ENABLED=False)
app.app.config.update(DEBUG=True)
client = app.app.test_client()


def test_routes():
    response = client.get('/')
    assert response.status_code == 200

    response = client.get('/test_routes')
    assert response.status_code == 404

    content = ('This is my unit test. '
               'There are many like it but this one is mine')
    with temp_file('templates/_test_routes.html', content):
        response = client.get('/test_routes')
        assert response.data.decode('utf8') == content

    response = client.get('/test_routes')
    assert response.status_code == 404


def test_reserved_routes():
    response = client.get('/login')
    data = response.data.decode('utf8')
    assert '<form action="/login" method="post">' in data

    response = client.get('/logout')
    assert response.status_code == 302

    with temp_file('templates/_login.html', 'no content'):
        response = client.get('/login')
        data = response.data.decode('utf8')
        assert '<form action="/login" method="post">' in data
        assert 'no content' not in data

    with temp_file('templates/_logout.html', 'no content'):
        response = client.get('/logout')
        assert response.status_code == 302

    response = client.get('/update-text')
    assert response.status_code == 404

    response = client.post('/update-text')
    assert response.status_code == 401


def test_login():
    pass
