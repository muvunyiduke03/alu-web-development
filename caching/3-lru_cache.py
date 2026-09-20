#!/usr/bin/env python3
"""LRUCache module.

This module defines a caching system that discards the least
recently used item once it exceeds the maximum number of items.
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """A caching system that removes items using an LRU policy."""

    def __init__(self):
        """Initialize the cache and its recency-order tracking."""
        super().__init__()
        self.__order = []

    def __mark_used(self, key):
        """Move key to the most-recently-used end of the order list."""
        if key in self.__order:
            self.__order.remove(key)
        self.__order.append(key)

    def put(self, key, item):
        """Add an item to the cache, evicting the LRU item if needed.

        Args:
            key: the key under which to store the item.
            item: the value to store.

        If key or item is None, this method does nothing. Putting a
        key (new or existing) marks it as the most recently used. If
        adding the item pushes the cache past BaseCaching.MAX_ITEMS,
        the least recently used key is discarded, and a message
        "DISCARD: <key>" is printed.
        """
        if key is None or item is None:
            return

        self.__mark_used(key)
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lru_key = self.__order.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD: {}".format(lru_key))

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key: the key to look up.

        Returns:
            The value linked to key, or None if key is None or
            doesn't exist in the cache.

        A successful lookup marks the key as the most recently used.
        """
        if key is None or key not in self.cache_data:
            return None
        self.__mark_used(key)
        return self.cache_data[key]
