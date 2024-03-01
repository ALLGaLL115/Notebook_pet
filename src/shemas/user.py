

from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
   email:str
   username:str
   password:str


class UserUpdate(BaseModel):
   email:str |None = None
   username:str |None = None
   password:str |None = None

class UserShema(BaseModel):
    id: int
    email: str
    username: str
    hashed_password: str
    created_at: datetime

class UserWithNotes(UserShema):
    notes: list["Note"]

