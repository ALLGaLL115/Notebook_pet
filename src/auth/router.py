from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, status, Depends, Body
from ..database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .shemas import UserBase, UserRead, UserCreate
from .crud_utils import insert_user, get_user



router = APIRouter(
    tags={"Auth"},
    prefix="/auth"
)

@router.post("/sing_up")
async def sing_up(user: Annotated[UserCreate, Body()], db: AsyncSession = Depends(get_async_session)):

        res = await insert_user(user=user, db = db)
        return {"response": res}
   

@router.get("sing_in")
async def sing_in(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_async_session))-> UserRead:
        
        user = get_user(username= username, password = password, db=db)
        
                
        return user
