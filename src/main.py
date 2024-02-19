from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from .database import get_async_session, Base
from pydantic import BaseModel  
from .auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)




























# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

# oauth2 = OAuth2PasswordBearer("token")
# def fake_hash_password(password: str):
#     return "fakehashed" + password

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# class UserInDB(User):
#     hashed_password:str

# # 
# def get_user(db:dict, username:str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token, db):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(db, token)
#     return user

# async def get_current_user(token: Annotated[str, Depends(oauth2)]):
#     user = fake_decode_token(token) 
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user

# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# app = FastAPI()


# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ):
#     user = get_user(fake_users_db, form_data.username)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     # user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/items")
# async def read_items(token: Annotated[str, Depends(oauth2)]):
#     return "items"

