#!/usr/bin/env python3
"""Web cache and tracker using Redis"""

import redis
import requests

r = redis.Redis()

num = 0


def get_page(url: str) -> str:
    """Obtain the HTML content of a given URL and track how many times it is accessed
       by incrementing a count stored in Redis with key 'count:{url}'
       Cache the result with an expiration time of 10 seconds using Redis 'setex'
       Return the HTML content of the URL
    """
    
    r.set(f"cached:{url}", num)
    
    resp = requests.get(url)
    
    r.incr(f"count:{url}")
    
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
