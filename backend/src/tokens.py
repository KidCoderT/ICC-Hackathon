from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError
import pickle

import models.schema
import rsa


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

pub_key = rsa.PublicKey(
    9850790067372835572933429070425433093012649905383235469423425640711972001150351396889583678238754399008474092995086523241692566140504123163012512889392089, 65537)
priv_key = rsa.PrivateKey(9850790067372835572933429070425433093012649905383235469423425640711972001150351396889583678238754399008474092995086523241692566140504123163012512889392089, 65537,
                          5375645146551140446318738380986239668256166916644430372590435854775515608294677840782473292571011451914956361322046609394865696061462845771834863606983313, 6384433107365408019045194750644174143660177780564146005695560298102483955129526879, 1542938879884019956938550730792157131003480093529048217093054520845345991)


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


def verify_token(token: str, exception, *args, **kwargs):
    try:
        payload = decrypt_token(token, *args, **kwargs)
        username = payload.get("sub")

        if username is not None:
            return models.schema.TokenData(username=username)  # type: ignore

        raise exception
    except JWTError as exc:
        raise exception from exc
