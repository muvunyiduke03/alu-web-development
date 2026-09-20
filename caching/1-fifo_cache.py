#!/usr/bin/env python3
"""FIFOCache module.

This module defines a caching system that discards the oldest
inserted item once it exceeds the maximum number of items.
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """A caching system that removes items using a FIFO policy."""

    def __init__(self):
        """Initialize the cache and its insertion-order tracking."""
        super().__init__()
        self.__order = []

    def put(self, key, item):
        """Add an item to the cache, evicting the oldest if needed.

        Args:
            key: the key under which to store the item.
            item: the value to store.

        If key or item is None, this method does nothing. If adding
        the item pushes the cache past BaseCaching.MAX_ITEMS, the
        first key ever inserted is discarded (FIFO), and a message
        "DISCARD: <key>" is printed.
        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.__order.append(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            oldest_key = self.__order.pop(0)
            del self.cache_data[oldest_key]
            print("DISCARD: {}".format(oldest_key))

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key: the key to look up.

        Returns:
            The value linked to key, or None if key is None or
            doesn't exist in the cache.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
