#!/usr/bin/env python3
""" Redis Module: This script demonstrates how to cache and count HTTP requests using Redis. """

from functools import wraps
import redis
import requests
from typing import Callable

# Create a Redis instance
redis_ = redis.Redis()

# Define a decorator to count the number of requests made to a specific URL
def count_requests(method: Callable) -> Callable:
    """ This decorator counts the number of requests made to a URL """
    @wraps(method)
    def wrapper(url):  
        """ This wrapper function is used to count the requests and cache the results """
        # Increment the count for the given URL
        redis_.incr(f"count:{url}")
        
        # Check if the result for the given URL is already cached in Redis
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            # Return the cached HTML
            return cached_html.decode('utf-8')
        
        # If the result is not cached, make a request to the URL
        html = method(url)
        
        # Cache the result for 10 seconds
        redis_.setex(f"cached:{url}", 10, html)
        
        # Return the HTML
        return html

    return wrapper


# Define a function to obtain the HTML content of a URL
@count_requests
def get_page(url: str) -> str:
    """ This function obtains the HTML content of a given URL """
    req = requests.get(url)
    return req.text
