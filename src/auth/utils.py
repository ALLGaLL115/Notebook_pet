# from ..auth.crud_utils import find_user_in_db, get_user
# from ..auth.shemas import Token, TokenData, UserInDB, UserRead

# from ..config import settings
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import datetime, timedelta, timezone
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from typing import Annotated
# from database import get_async_session

# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_acces_token(data:dict, expires_delta: timedelta|None = None):
#     to_encode= data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encode_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
#     return encode_jwt

    

# async def get_current_user(db:AsyncSession, token: Annotated[str, Depends(oauth2_scheme)]):
#     credential_exeption = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Couldnt validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credential_exeption
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credential_exeption
#     user_db = find_user_in_db(username=token_data.username, db = db).__delattr__("hashed_password")
#     if user_db is None:
#         raise credential_exeption
#     return UserRead(**user_db.__dict__)







        
