

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
from models import User
from shemas.token import TokenData
from shemas.user import UserShema
from utils.hashing import verify_password
from utils.repository import SQLAlchemyRepository



class UserRepository(SQLAlchemyRepository):
    model = User


    async def get_current_user(
            self,
            token: str,
           
        )->UserShema:
            credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise credentials_exception
                token_data = TokenData(username=username)
            except JWTError:
                raise credentials_exception

            user = await self.get_one(filters={"username":token_data.username})
            if user is None:
                raise credentials_exception
            return user
            
    async def authenticate_user(self, username:str, password:str) -> UserShema:
    
        filter_dict= {"username":username, "password":password}
        user_db = await  self.get_one(filters={"username":username})

        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not registrated")
        
        if not verify_password(plain_password=password, hashed_password=user_db.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong password")
        res = user_db.convert_to_model()
        return res