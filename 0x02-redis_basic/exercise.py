#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Union


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
