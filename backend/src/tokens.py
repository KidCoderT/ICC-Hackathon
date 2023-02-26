from typing import Optional
from datetime import timedelta, datetime
from jose import jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates an access token using the given data and optional expiration time.
    Parameters:
     - data: dict: The data to be included in the access token.
     - expires_delta: Optional[timedelta]: The amount of time until the access token expires.
     - If not provided, the token will expire in the number of minutes specified by the
     - ACCESS_TOKEN_EXPIRE_MINUTES constant.
    Returns - str: The encoded access token.
    """

    to_encode = data.copy()

    expire = datetime.utcnow()
    expire += (
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if expires_delta is None
        else expires_delta
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decrypt_token(token: str, *args, **kwargs):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], *args, **kwargs)


# def verify_token(token: str, exception, *args, **kwargs) -> models.schema.TokenData:
#     """Verifies the given token.
#     Parameters:
#         - token (str): The token to be verified.
#         - exception: The exception to be raised if the token is invalid.
#     Returns: - models.schema.TokenData: The data stored in the token.
#     Raises: - exception: If the token is invalid.
#     """
#     try:
#         payload = decrypt_token(token, *args, **kwargs)
#         email = payload.get("sub")

#         if email is not None:
#             return models.schema.TokenData(email=email)  # type: ignore

#         raise exception
#     except JWTError as exc:
#         raise exception from exc