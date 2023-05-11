import requests
import redis

cache = redis.Redis()


def count_calls(method):
    """Decorator to count the number of times a method is called."""
    def wrapper(*args, **kwargs):
        url = args[0]
        cache.incr(f"count:{url}")
        return method(*args, **kwargs)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL and caches the result for 10 seconds."""
    key = f"content:{url}"
    content = cache.get(key)
    if content is None:
        print(f"Fetching {url}...")
        response = requests.get(url)
        content = response.content
        cache.setex(key, 10, content)
    else:
        print(f"Using cached content for {url}")
    return content.decode("utf-8")
