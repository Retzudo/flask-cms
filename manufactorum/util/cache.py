"""Cache handling utilities."""
from manufactorum import app
import redis
import sys
from redis.exceptions import ConnectionError

CACHE_LIST_KEY = '#cached_paths#'


def get_redis():
    if app.config['REDIS_SOCKET']:
        return redis.Redis(unix_socket_path=app.config['REDIS_SOCKET'])
    else:
        return redis.Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            socket_timeout=app.config['REDIS_TIMEOUT']
        )


def redis_wrapper(redis_action):
    """Try to connect to redis. If no connection is available return None."""
    def wrapper(*args, **kwargs):
        try:
            return redis_action(*args, **kwargs)
        except ConnectionError:
            print(
                'Could not connect to redis on {}:{}. Caching unavailable.'
                .format(app.config['REDIS_HOST'], app.config['REDIS_PORT']),
                file=sys.stderr
            )
            return None

    return wrapper


@redis_wrapper
def delete_all_paths():
    """Delete content for all cached paths."""
    for p in get_redis().lrange(CACHE_LIST_KEY, 0, -1):
        get_redis().delete(p)
    get_redis().delete(CACHE_LIST_KEY)


@redis_wrapper
def delete_path(path):
    """
    Deletes the cache entries for all cached paths or a specific cached path.
    """
    get_redis().delete(path)


@redis_wrapper
def cache_path(path, html):
    """Cache the content for a path."""
    get_redis().set(path, html)
    get_redis().lpush(CACHE_LIST_KEY, path)


@redis_wrapper
def get_path(path):
    """Retrieve cached content of a path."""
    return get_redis().get(path)
