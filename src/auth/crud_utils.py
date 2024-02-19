from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy import and_, insert, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from ..config import settings
from .shemas import Token, TokenData, UserCreate, UserRead, UserInDB
from .models import UserTable
from ..database import get_async_session
# from .utils import get_password_hash, verify_password


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def find_user_in_db(db:AsyncSession, username:str|None, )->UserInDB|None:
    query = (
        select(UserTable)
        .filter_by(username=username)
    ) 
    res = await db.execute(query)
    user = res.scalar_one_or_none()
    if user is None:
        return user
    return UserInDB(**user.__dict__)

async def authenticate_user(db:AsyncSession, username:str, password:str) :
    user = await find_user_in_db(db,username)
    if user is None: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user not registrated")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong Pasword")
    return user

async def registrate_user(db:AsyncSession, user:UserCreate):
    user_db = await  find_user_in_db(db, user.username)
    if user_db:
        if user_db.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This username is already used")
        # if user_db.email == user.email:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already used")

    
    hashed_password = get_password_hash(user.password)
    user_input = user.model_dump(exclude={"password"})
    user_input.update({"hashed_password": hashed_password})
    
    stmt = insert(UserTable).values(user_input)

    res = await db.execute(stmt)
    
    await db.commit()
    return {"status":200, "detail":"User registrated"}
        

    
        



    




def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_acces_token(data:dict, expires_delta: timedelta|None = None):
    to_encode= data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

    

async def get_current_user(db:Annotated[AsyncSession, Depends(get_async_session)], token: Annotated[Token, Depends(oauth2_scheme)]) :
    credential_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldnt validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exeption
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exeption
    user_db = await find_user_in_db(username=token_data.username, db = db)
       
    
    return  UserRead(
        id= user_db.id,
        # email= user_db.email,
        username= user_db.username
    )
    


async def get_current_active_user(
    current_user: Annotated[Token, Depends(get_current_user)]
):
       return current_user







        
