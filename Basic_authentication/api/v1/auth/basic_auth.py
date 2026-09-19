#!/usr/bin/env python3
"""Module that manages Basic Authentication for the API."""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class.

    Implements the actual Base64 decode-and-match logic that the
    Auth base class leaves as placeholders, so requests can be
    verified against a username/password pair sent in the
    Authorization header.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header.

        Given a header like "Basic <base64string>", returns just
        the <base64string> portion. Returns None if the header is
        missing, not a string, or doesn't start with "Basic ".
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode a Base64 string into its original UTF-8 string.

        Returns None if the input is missing, not a string, or is
        not valid Base64 (e.g. corrupted or tampered with).
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Split a decoded 'email:password' string into its parts.

        Returns (email, password) as a tuple, or (None, None) if
        the input is missing, not a string, or has no ':' separator.
        Only splits on the FIRST ':', so passwords containing a
        colon are preserved intact.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(
            ':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return the User instance matching the given credentials.

        Looks up users by email, then checks the password against
        the stored hash. Returns None if either value is missing,
        not a string, no user matches the email, or the password
        is wrong.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the authenticated User for the current request.

        Chains together every step above: reads the Authorization
        header, extracts and decodes the Base64 portion, splits
        out the email/password, and resolves the matching User.
        Returns None if any step along the way fails.
        """
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(
            auth_header)
        decoded = self.decode_base64_authorization_header(b64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(user_email, user_pwd)
