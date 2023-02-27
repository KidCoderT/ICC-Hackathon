import re
from typing import Union
from passlib.context import CryptContext

CRYPT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verifies that the given plain text password matches the given hashed password.
    Parameters:
        - plain_password: str: The plain text password to verify.
        - hashed_password: str: The hashed password to check against.
    Returns: - bool: True if the given plain text password matches the
                given hashed password, False otherwise.
    """
    return CRYPT_CONTEXT.verify(plain_password, hashed_password)


def hash_password(password):
    """Hashes the given password using the bcrypt algorithm.
    Parameters: - password: str: The password to hash.
    Returns: - str: The hashed password.
    """
    return CRYPT_CONTEXT.hash(password)
