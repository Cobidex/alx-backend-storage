#!/usr/bin/env python3
"""
Cache module
"""
from functools import wraps
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

    def count_calls(self, func: Callable) -> Callable:
        """
        count how many times methods of the Cache class are called
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self._redis.incr(func.__qualname__)
            return func(self, *args, **kwargs)
        return wrapper

    def call_history(method):
        """
        store the history of inputs and outputs for a particular function
        """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)
        return output
    return wrapper

    def replay(func):
        """
        display the history of calls of a particular function
        """
    inputs_key = "{}:inputs".format(func.__qualname__)
    outputs_key = "{}:outputs".format(func.__qualname__)
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)
    num_calls = len(inputs)

    print("{} was called {} times:".format(func.__qualname__, num_calls))

    for i, (input_str, output_str) in enumerate(zip(inputs, outputs)):
        input_args = eval(input_str.decode("utf-8"))  # Convert string back to tuple
        output = output_str.decode("utf-8")
        print("{}(*{}) -> {}".format(func.__qualname__, input_args, output))
