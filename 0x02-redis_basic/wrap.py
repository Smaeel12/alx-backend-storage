#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable, Optional

# Redis connection
redis_store = redis.Redis()
'''The module-level Redis instance.'''

RESULT_KEY_PREFIX = 'result:'
COUNT_KEY_PREFIX = 'count:'

def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data from a URL.
    
    Args:
        method (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function with caching behavior.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.
        
        Args:
            url (str): The URL to fetch.

        Returns:
            str: The content of the URL.
        '''
        redis_store.incr(f'{COUNT_KEY_PREFIX}{url}')
        result: Optional[bytes] = redis_store.get(f'{RESULT_KEY_PREFIX}{url}')
        
        if result:
            return result.decode('utf-8')
        
        try:
            result = method(url)
            redis_store.set(f'{COUNT_KEY_PREFIX}{url}', 0)
            redis_store.setex(f'{RESULT_KEY_PREFIX}{url}', 10, result)
            return result
        except requests.RequestException as e:
            print(f"Error fetching the URL {url}: {e}")
            return "Error fetching data"  # Return an error message or handle appropriately

    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The content of the page.
    '''
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response was an error
    return response.text

