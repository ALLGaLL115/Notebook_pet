from pydantic import BaseModel

class UserBase(BaseModel):
    username:str

class UserCreate(UserBase):
    password: str
    # email: str

class UserRead(UserBase):
    id:int
    # email:str

class UserInDB(UserRead):
    hashed_password:str




class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str