#!/usr/bin/env python3

import redis
import time
from web import get_page
r = redis.Redis()
url = "http://github.com"
text = get_page(url)
print("returned text is :")
print()
print(text)

print("number of times accessed in 10s:")
print(r.get(f"count:{url}").decode("utf-8"))
get_page(url)
print(r.get(f"count:{url}").decode("utf-8"))
get_page(url)

print(r.get(f"count:{url}").decode("utf-8"))
get_page(url)
get_page(url)
get_page(url)
get_page(url)
time.sleep(11)
print("after 10s:")
print(r.get(f"count:{url}"))
