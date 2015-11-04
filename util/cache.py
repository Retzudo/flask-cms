"""Cache handling utilities."""
import redis
import settings

rd = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
CACHE_LIST_KEY = '#cached_paths#'


def delete_all_paths():
    """Delete content for all cached paths."""
    for p in rd.lrange(CACHE_LIST_KEY, 0, -1):
        rd.delete(p)
    rd.delete(CACHE_LIST_KEY)


def delete_path(path):
    """
    Deletes the cache entries for all cached paths or a specific cached path.
    """
    rd.delete(path)


def cache_path(path, html):
    """Cache the content for a path."""
    rd.set(path, html)
    rd.lpush(CACHE_LIST_KEY, path)


def get_path(path):
    """Retrieve cached content of a path."""
    return rd.get(path)
