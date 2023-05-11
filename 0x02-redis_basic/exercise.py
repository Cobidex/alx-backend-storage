#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """
    Cache class that stores data in Redis
    """
    def __init__(self):
        """
        Initializes Redis client and flushes the instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis using the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the value for the given key from Redis and applies the given function to the value if provided
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves the string value for the given key from Redis
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves the integer value for the given key from Redis
        """
        return self.get(key, fn=int)
