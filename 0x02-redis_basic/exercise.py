#!/usr/bin/env python3
""" Writing strings to Redis 
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps

def _redis_key(method_name: str, suffix: str) -> str:
    """Utility function to generate Redis keys."""
    return f"{method_name}:{suffix}"

def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.'''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Returns the given method after incrementing its call counter.'''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.'''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.'''
        if isinstance(self._redis, redis.Redis):
            in_key = _redis_key(method.__qualname__, 'inputs')
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            out_key = _redis_key(method.__qualname__, 'outputs')
            self._redis.rpush(out_key, str(output))  # Ensure output is a string
        return output
    return invoker

def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.'''
    if fn is None or not hasattr(fn, '__self__'):
        return
    
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    
    fxn_name = fn.__qualname__
    fxn_call_count = redis_store.get(fxn_name) or 0

    print(f'{fxn_name} was called {fxn_call_count} times:')
    
    in_key = _redis_key(fxn_name, 'inputs')
    out_key = _redis_key(fxn_name, 'outputs')
    
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print(f'{fxn_name}(*{fxn_input.decode("utf-8")}) -> {fxn_output.decode("utf-8")}')


class Cache:
    """ Represents an object for storing data in a Redis data storage.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores a value in a Redis data storage and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key 

    def get(self, key: str, fn: Callable=None) -> None:
        """ Retrieves a value from a Redis data storage.
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """ Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """ Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
