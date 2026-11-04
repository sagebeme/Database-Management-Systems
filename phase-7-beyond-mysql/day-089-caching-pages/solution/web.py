"""Day 89: an expiring page cache.

`client` is a redis.Redis connection.
"""

from urllib.request import urlopen


def fetch(url):
    """Download a page and return its text. Slow: it goes over the network. (Done for you.)"""
    with urlopen(url, timeout=10) as response:
        return response.read().decode("utf-8")


def get_page(client, url, seconds=10):
    """The page's text, from the cache at cached:<url> if it's there, otherwise from fetch(url), then cached for
    `seconds` seconds. Count every call, cached or not, at count:<url>."""
    client.incr(f"count:{url}")
    cached = client.get(f"cached:{url}")
    if cached is not None:
        return cached.decode("utf-8")
    page = fetch(url)
    client.set(f"cached:{url}", page, ex=seconds)
    return page
