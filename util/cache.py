"""Cache handling utilities."""
import redis
import settings
import sys
from redis.exceptions import ConnectionError


rd = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

CACHE_LIST_KEY = '#cached_paths#'


def redis_wrapper(redis_action):
    """Try to connect to redis. If no connection is available return None."""
    def wrapper(*args, **kwargs):
        try:
            return redis_action(*args, **kwargs)
        except ConnectionError:
            print(
                'Could not connect to redis on {}:{}. Caching unavailable.'
                .format(settings.REDIS_HOST, settings.REDIS_PORT),
                file=sys.stderr
            )
            return None

    return wrapper


@redis_wrapper
def delete_all_paths():
    """Delete content for all cached paths."""
    for p in rd.lrange(CACHE_LIST_KEY, 0, -1):
        rd.delete(p)
    rd.delete(CACHE_LIST_KEY)


@redis_wrapper
def delete_path(path):
    """
    Deletes the cache entries for all cached paths or a specific cached path.
    """
    rd.delete(path)


@redis_wrapper
def cache_path(path, html):
    """Cache the content for a path."""
    rd.set(path, html)
    rd.lpush(CACHE_LIST_KEY, path)


@redis_wrapper
def get_path(path):
    """Retrieve cached content of a path."""
    return rd.get(path)
