from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .shemas import Token, UserBase, UserInDB, UserCreate, UserRead
from .crud_utils import create_acces_token, get_current_active_user, get_current_user, registrate_user, authenticate_user
# from .utils import create_acces_token, get_current_user
from ..config import settings



router = APIRouter(
    tags={"Auth"},
#     prefix="auths"
    
)
# @router.post("/token")
# def get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     return "dsf"


# @router.get("masdf")
# def get(token:Annotated[str, OAuth2PasswordBearer(tokenUrl="token")]):
#     return""

@router.post("/sing_up")
async def sing_up(user: Annotated[UserCreate, Body()], db: AsyncSession = Depends(get_async_session)):

        res = await registrate_user(user=user, db = db)
        return {"response": res}
   

@router.post("/token")
async def login_for_access_token(
form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_async_session))->Token:
        
        user =await authenticate_user(db, username=form_data.username, password=form_data.password)
        
        if not user:
                raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"},
                                )
        access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)    
        access_token = create_acces_token(
                data={"sub":user.username},
                expires_delta=access_token_expire
        )
                        
        return Token(access_token= access_token, token_type="bearer")


@router.get("/chk_token")
async def check_token(token: Annotated[Token, Depends(get_current_user)]):
        return token

# @router.get()
@router.get("/hehe")      
async def login_for_access_token(
        form_data: Annotated[UserRead, Depends(get_current_active_user)],
        db:AsyncSession= Depends(get_async_session)
) :
        return{"status":200}
        