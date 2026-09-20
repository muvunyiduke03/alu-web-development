#!/usr/bin/env python3
"""BasicCache module.

This module defines a simple caching system with no size limit,
built on top of BaseCaching.
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """A caching system that has no limit on the number of items."""

    def put(self, key, item):
        """Add an item to the cache.

        Args:
            key: the key under which to store the item.
            item: the value to store.

        If key or item is None, this method does nothing.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

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
