#!/usr/bin/env python3
"""LFUCache module.

This module defines a caching system that discards the least
frequently used item once it exceeds the maximum number of items,
breaking ties with the least recently used item.
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """A caching system that removes items using an LFU policy,
    falling back to LRU to break frequency ties.
    """

    def __init__(self):
        """Initialize the cache, its frequency and recency tracking."""
        super().__init__()
        self.__freq = {}
        self.__order = []

    def __mark_used(self, key):
        """Move key to the most-recently-used end of the order list."""
        if key in self.__order:
            self.__order.remove(key)
        self.__order.append(key)

    def put(self, key, item):
        """Add an item to the cache, evicting the LFU item if needed.

        Args:
            key: the key under which to store the item.
            item: the value to store.

        If key or item is None, this method does nothing. Each put
        to a key (new or existing) increases its usage frequency by
        one and marks it as the most recently used. If adding a new
        key pushes the cache past BaseCaching.MAX_ITEMS, the least
        frequently used key among the previously existing items is
        discarded (the newly inserted key is never itself the
        target), breaking ties with the least recently used of that
        group, and a message "DISCARD: <key>" is printed.
        """
        if key is None or item is None:
            return

        self.__freq[key] = self.__freq.get(key, 0) + 1
        self.__mark_used(key)
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            candidates = [k for k in self.cache_data if k != key]
            min_freq = min(self.__freq[k] for k in candidates)
            lfu_keys = {k for k in candidates if self.__freq[k] == min_freq}

            discard_key = None
            for k in self.__order:
                if k in lfu_keys:
                    discard_key = k
                    break

            self.__order.remove(discard_key)
            del self.cache_data[discard_key]
            del self.__freq[discard_key]
            print("DISCARD: {}".format(discard_key))

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key: the key to look up.

        Returns:
            The value linked to key, or None if key is None or
            doesn't exist in the cache.

        A successful lookup increases the key's usage frequency and
        marks it as the most recently used.
        """
        if key is None or key not in self.cache_data:
            return None
        self.__freq[key] = self.__freq.get(key, 0) + 1
        self.__mark_used(key)
        return self.cache_data[key]
