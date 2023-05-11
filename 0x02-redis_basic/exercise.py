#!/usr/bin/env python3
"""
Redis Cache exercise
"""
import uuid
from typing import Callable, Any
import redis


class Cache:
    """
    Cache class
    """
    def __init__(self):
        """
        Initializes a new instance of the Cache class
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)

    def store(self, data: Any) -> str:
        """
        Generates a new UUID, stores the data with that UUID as key
        and returns the UUID
        """
        key = str(uuid.uuid4())
        self._redis.set(key, str(data))
        return key


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a particular function
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapper function that will store the input and output history
        """
        key_inputs = "{}:inputs".format(method.__qualname__)
        key_outputs = "{}:outputs".format(method.__qualname__)
        normalized_args = str(args)
        # Append the input arguments to the Redis list
        method._redis.rpush(key_inputs, normalized_args)
        # Execute the wrapped function to retrieve the output
        output = method(*args, **kwargs)
        # Store the output using rpush in the "...:outputs" list
        method._redis.rpush(key_outputs, output)
        # Return the output
        return output
    return wrapper


@call_history
def cached_function(x: int) -> int:
    """
    A sample function to test the call_history decorator
    """
    return x * 2


def replay(func: Callable) -> None:
    """
    Displays the history of calls of a particular function
    """
    key_inputs = "{}:inputs".format(func.__qualname__)
    key_outputs = "{}:outputs".format(func.__qualname__)
    inputs = func._redis.lrange(key_inputs, 0, -1)
    outputs = func._redis.lrange(key_outputs, 0, -1)
    num_calls = len(inputs)
    print("{} was called {} times:".format(func.__name__, num_calls))
    for i, (input_str, output_str) in enumerate(zip(inputs, outputs)):
        input_args = eval(input_str.decode('utf-8'))
        output = output_str.decode('utf-8')
        print("{}(*{}) -> {}".format(func.__name__, input_args, output))


if __name__ == '__main__':
    cache = Cache()
    s1 = cache.store("first")
    s2 = cache.store("secont")
    s3 = cache.store("third")
    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)
    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
    replay(cached_function)
