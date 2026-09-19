#!/usr/bin/env python3
"""Module that manages the API authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template class for all authentication systems used by the API.

    Subclasses (like BasicAuth) will override these methods with
    real logic. On its own, this class allows every request through
    unauthenticated, which is why it's the safe default to inherit
    from before any real auth is wired in.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine whether a given path requires authentication.

        Returns False (no auth needed) only if path exactly matches
        one of excluded_paths, ignoring a trailing slash difference
        between the two. Returns True (auth needed) for every other
        path, and also if path or excluded_paths is missing/empty.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path = path + '/'
        for excluded_path in excluded_paths:
            normalized = excluded_path
            if not normalized.endswith('/'):
                normalized = normalized + '/'
            if path == normalized:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the value of the request's Authorization header.

        Returns None if request is missing or has no Authorization
        header set. Otherwise returns the raw header value exactly
        as the client sent it (e.g. "Basic <base64string>").
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the User instance for the current request.

        Currently always returns None. Subclasses override this to
        resolve and return the authenticated User based on the
        request's credentials.
        """
        return None
