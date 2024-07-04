#!/usr/bin/env python3
"""Module encrypts passwords """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """displays the has password function """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ password validator"""
    return bcrypt.checkpw(password.encode(), hashed_password)
