from manufactorum import app
from manufactorum.util import cache
from unittest.mock import patch


def test_cache():
    cache.cache_path('/testpath', 'content')
    assert cache.get_path('/testpath') == b'content'
    cache.delete_path('/testpath')
    assert cache.get_path('/testpath') is None

    cache.cache_path('/testpath1', 'content')
    cache.cache_path('/testpath2', 'content')
    cache.cache_path('/testpath3', 'content')
    cache.delete_all_paths()

    assert cache.cache_path('/testpath1', 'content') is None
    assert cache.cache_path('/testpath2', 'content') is None
    assert cache.cache_path('/testpath3', 'content') is None


def test_without_redis():
    config = {
        'REDIS_HOST': 'example.com',
        'REDIS_PORT': 9999,
        'REDIS_TIMEOUT': 0.1
    }
    with patch.dict('manufactorum.app.config', config):
        cache.cache_path('/testpath', 'content')
        assert cache.get_path('/testpath') is None
