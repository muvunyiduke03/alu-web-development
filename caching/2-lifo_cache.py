#!/usr/bin/env python3
"""LIFOCache module.

This module defines a caching system that discards the most
recently inserted item once it exceeds the maximum number of items.
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """A caching system that removes items using a LIFO policy."""

    def __init__(self):
        """Initialize the cache and its insertion-order tracking."""
        super().__init__()
        self.__order = []

    def put(self, key, item):
        """Add an item to the cache, evicting the newest if needed.

        Args:
            key: the key under which to store the item.
            item: the value to store.

        If key or item is None, this method does nothing. Re-putting
        an existing key refreshes its position as the most recent
        entry. If adding the item pushes the cache past
        BaseCaching.MAX_ITEMS, the last key that was put in the
        cache before this one is discarded (LIFO), and a message
        "DISCARD: <key>" is printed.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.__order.remove(key)

        self.__order.append(key)
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discard_key = self.__order.pop(-2)
            del self.cache_data[discard_key]
            print("DISCARD: {}".format(discard_key))

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
