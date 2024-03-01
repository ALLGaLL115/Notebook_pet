

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from utils.unit_of_work import IUnitOfWork, UnitOfWork


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

TokenDep = Annotated[str, Depends(oauth2_scheme)]