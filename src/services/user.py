

from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from config import settings
from shemas.token import Token
from shemas.user import UserCreate, UserShema, UserUpdate
from utils.jwt_tokens import create_access_token
from utils.unit_of_work import IUnitOfWork
from utils.hashing import hash_password



class UserService:

    async def create_user(self, uow:IUnitOfWork, user:UserCreate):
        async with uow:
            user_data: dict = user.model_dump()
            hashed_password = hash_password(user_data["password"])
            del user_data["password"]
            user_data["hashed_password"] = hashed_password

            
            
            id = await uow.users.add_one(user_data)

            if id is None:
                await uow.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")
            await uow.commit()
            return {"status":200, "detail":"User was created"}
        

    async def login(
            self,
            uow:IUnitOfWork,
            form_data:OAuth2PasswordRequestForm):
        
            async with uow:
                try:
                    user_db = await uow.users.authenticate_user(username=form_data.username, password=form_data.password)
                    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                    access_token = create_access_token(data={"sub":user_db.username}, expires_delta=access_token_expires)
                    
                    await uow.commit()
                    return Token(access_token = access_token, token_type = "bearer")
                except HTTPException as e:
                    await uow.rollback()

                    raise e
        
    

            
    
    
    async def update_user(self, uow:IUnitOfWork, updates:UserUpdate, token:str):        
        base_updates_dict = updates.model_dump()
        valid_updates_dict = {k:v for k, v in base_updates_dict.items() if v is not None}
        if len(valid_updates_dict) == 0:
            raise HTTPException(status_code=status, detail="Add some updates")

        if "password" in valid_updates_dict:
            hashed_password = hash_password(valid_updates_dict["password"])
            del valid_updates_dict["password"]
            valid_updates_dict["hashed_password"] = hashed_password

        async with uow:
            try:    
                if "email" in valid_updates_dict:
                    user_current = await uow.users.get_current_user(token)

                    if user_current.email == valid_updates_dict["email"]:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already use this email")


                    user_check = await uow.users.get_one(filters={"email": valid_updates_dict["email"]})
                    if user_check is not None:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already used")


                user_db = await uow.users.get_current_user(token=token)


                res = await uow.users.update_one(id=user_db.id, update_data=valid_updates_dict)
                if res is None:
                    raise HTTPException(status_code=500, detail="Server error")
                
                if "username" in valid_updates_dict:
                    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                    access_token = create_access_token(data={"sub":user_db.username}, expires_delta=access_token_expires)
                   
                    # await uow.commit()
                    return {"status":200, "detail":"User and access token was updated", "data":f"{access_token}"}
                
                
                # await uow.commit()
                return {"status":200, "detail":"User was updated",}
            except HTTPException as e:
                await uow.rollback()
                raise e 
            except BaseException as be:
                await uow.rollback()
                print(be)
                raise HTTPException(status_code=500, detail="Server error") 


    async def delete_user(self, uow:IUnitOfWork, token:str):
        async with uow:
            try:
                user = await uow.users.get_current_user(token)
                
                res = await uow.users.delete_one(id=user.id)
                await uow.commit()
                return {"status":200, "detail": f"User with id {res} was deleted"}
            except HTTPException as e:
                await uow.rollback()
                raise e

        

        
                

    # async def get_one(self, uow:IUnitOfWork, user_id:int, ):
    #     async with uow:
    #         res = await uow.users.get_one(table_id=user_id)
    #         # if res is None:

    #         #     raise HTTPException(status_code=500, detail="server error")
    #         return res
        
   
    