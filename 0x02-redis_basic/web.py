#!/usr/bin/env python3
"""Web cache and tracker using Redis"""

import redis
import requests

# Create a Redis client instance
r = redis.Redis()

# Set a variable to keep track of URL counts
count = 0


def get_page(url: str) -> str:
    """Obtain the HTML content of a given URL and track how many times it is accessed
       by incrementing a count stored in Redis with key 'count:{url}'
       Cache the result with an expiration time of 10 seconds using Redis 'setex'
       Return the HTML content of the URL"""
    
    # Store the count for the given URL in Redis
    r.set(f"cached:{url}", count)
    
    # Send a GET request to the URL
    resp = requests.get(url)
    
    # Increment the count for the URL in Redis
    r.incr(f"count:{url}")
    
    # Cache the HTML content in Redis with an expiration time of 10 seconds
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    
    # Return the HTML content of the URL
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
