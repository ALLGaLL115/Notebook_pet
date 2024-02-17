from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email:str 
    password: str

class UserLogin(UserBase):
    password:str

class UserRead(UserBase):
    id:int
    email:str