#!/usr/bin/env python3

from typing import Callable, Optional, Union
from uuid import uuid4
import redis
from functools import wraps

'''
    A function to write strings to Redis.
'''


def count_function_calls(function: Callable) -> Callable:
    '''
        A decorator to count the number of times a function is called.
    '''

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        '''
            A wrapper function for counting function calls.
        '''
        key = function.__qualname__
        self._redis.incr(key)
        return function(self, *args, **kwargs)
    return wrapper


def log_function_calls(method: Callable) -> Callable:
    """ A decorator to log the history of inputs and outputs for a particular function. """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay_function_calls(function: Callable) -> None:
    # A function to replay the history of a particular function
    name = function.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    '''
        A Cache class.
    '''
    def __init__(self):
        '''
            Initializes the cache.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_function_calls
    @log_function_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            Stores data in the cache.
        '''
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''
            Gets data from the cache.
        '''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''
            Gets a string from the cache.
        '''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        '''
            Gets an int from the cache.
        '''
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
