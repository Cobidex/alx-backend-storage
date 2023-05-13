#!/usr/bin/env python3
"""Web cache and tracker using Redis"""

import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()
count = 0


def count_access(method: Callable) -> Callable:
    """
    decorator method to get count of number of times url is assessed
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        """
        wrapper function around the method
        """
        url = args[0]
        r.setnx(f"count:{url}", count)
        r.incr(f"count:{url}")
        r.setex(f"count:{url}", 10, r.get(f"count:{url}"))
        return method(*args, **kwargs)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a given URL and track how many
    times it is accessed
    by incrementing a count stored in Redis with key
    'count:{url}'
    Cache the result with an expiration time of 10 seconds
    using Redis 'setex'
    Return the HTML content of the URL
    """
    resp = requests.get(url)
    return resp.text
