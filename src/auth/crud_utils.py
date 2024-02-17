from sqlalchemy import insert, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .shemas import UserCreate, UserLogin, UserRead
from .models import User
from .utils import get_password_hash

async def insert_user(user: UserCreate, db: AsyncSession):
    search_user = (
        select(User)
        .filter((User.email == user.email) | (User.username == user.username))
    )

    search_result = await db.execute(search_user)
    search_model = search_result.scalar()
    if not search_model is None:
        if search_model.email == user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "This email is already used")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already used")
    
    hased_password = get_password_hash(user.password)
    stmt = insert(User).values(
        {"email":user.email, "username":user.username, "hashed_password": hased_password})
    
    res = await db.execute(stmt)
    
    await db.commit()
    return {"status":200, "detail": "User have been created"}


async def get_user(user:UserLogin, db:AsyncSession)->UserRead:
    query = (
        select(User)
        .filter_by(username = user.username)
    )

    response = await db.execute(query)
    user_db = response.scalar_one_or_none()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not registered")
    
    hashed_password = get_password_hash(user.password)

    if hashed_password != user_db.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    
    
        
    return UserRead(id=user_db.id, username=user_db.username, email=user_db.email)
    


