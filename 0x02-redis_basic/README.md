# Request Caching and Tracking Module

This module provides a caching mechanism for HTTP requests using Redis. It tracks the number of times a URL has been requested and caches the response for a specified duration. This is useful for reducing redundant network calls and improving application performance.

## Features

- Caches HTTP response data for quick retrieval.
- Tracks the number of requests made to each URL.
- Handles network errors gracefully.

## Requirements

- Python 3.7
- Redis server
- `requests` library
- `redis` library

## Usage

1. Import the `get_page` function.
2. Call `get_page(url)` to retrieve the content of a URL.

## Example

```python
content = get_page('http://example.com')
print(content)

