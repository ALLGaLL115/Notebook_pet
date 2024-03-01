
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.dependecies import UOWDep, TokenDep
from services.user import UserService

from shemas.user import UserCreate, UserShema, UserUpdate
router = APIRouter(
    tags=["User"],
    prefix="/user"
)

@router.post("/sing_up")
async def add_user(user: UserCreate, uow:UOWDep):
    
    res = await UserService().create_user(uow, user)
    return res


@router.post("/token")
async def sing_in(
        uow:UOWDep,
        form_data:Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    res = await UserService().login(
        uow=uow,
        form_data=form_data)
    return res

@router.post("/updates")
async def update_user(
    uow:UOWDep,
    updates:UserUpdate,
    token: TokenDep
    ):
    res = await UserService().update_user(uow, updates, token)
    return res
    

@router.post("/del")
async def delet_user(uow:UOWDep, token: TokenDep):
    res = await UserService().delete_user(uow, token)
    return res






