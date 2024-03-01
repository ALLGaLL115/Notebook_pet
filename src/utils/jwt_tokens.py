from typing import Annotated
from fastapi import Depends

from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from config import settings

def create_access_token(data: dict, expires_delta: timedelta| None = None):

    to_encode = data.copy()
    if expires_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    else:
        expire =  datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt



