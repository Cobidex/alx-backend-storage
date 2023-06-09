#!/usr/bin/env python3
"""
Web cache and tracker using Redis
"""

import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def count_access(method: Callable[..., str]) -> Callable[..., str]:
    """
    decorator method to get count of number of times url is assessed
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        wrapper function around the method
        """
        cached_result: bytes = r.get(f"cache:{url}")
        if cached_result:
            return cached_result.decode("utf-8")
        result: str = method(url)
        r.incr(f"count:{url}")
        r.setex(f"cache:{url}", 10, result)
        return result
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a given URL and track how many
    Return the HTML content of the URL
    """
    resp: requests.Response = requests.get(url)
    return resp.text
