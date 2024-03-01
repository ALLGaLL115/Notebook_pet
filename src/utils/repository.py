from abc import ABC, abstractclassmethod
from venv import logger
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from exeptions import sql_exeption

from sqlalchemy import select, insert, update, delete
class AbstractRepository(ABC):

    @abstractclassmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractclassmethod
    async def get_one():
        raise NotImplementedError
    
    @abstractclassmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractclassmethod
    async def delete_one():
        raise NotImplementedError
    


class SQLAlchemyRepository(AbstractRepository):


    model = None

    def __init__(self, session: AsyncSession):
        self.session = session



    async def add_one(self, data:dict,)->int:
        try:
            stmt = insert(self.model).values(**data)
            res = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            logger.exception(f"Adding error {e}")
            raise sql_exeption


    async def get_all(self, filter:dict):
        try:
            stmt = select(self.model).filter_by(**filter)
            res = await self.session.execute(stmt)
            models = [model.convert_to_model for model in res.scalars().all()]
            return models
        except SQLAlchemyError as e:
            logger.exception(
                f"Getting error"
                f"Error -> {e}"
            )
            raise sql_exeption


    # async def get_one_by_id(self, id: int, model=None):
    #     model = model or self.model
    #     stmt = select(model).filter_by(id=id)
    #     res = await self.session.execute(stmt)
    #     return res.scalar_one()

    async def get_one(self, filters:dict):
        try:
            stmt = select(self.model).filter_by(**filters)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res
        
        except SQLAlchemyError as e:
            logger.exception(
                f"Getting error"
                f"Error -> {e}"
            )
            raise sql_exeption



    # async def get_one(self, table_id:int):
    #     stmt = select(self.model).filter_by(id=table_id)
    #     res = await self.session.execute(stmt)
    #     res = res.scalar_one()
    #     print(f"{res=}")
    #     return res.convert_to_model()
             
    async def delete_one(self, id:int):
        try:
            stmt = delete(self.model).filter_by(id=id)
            await self.session.execute(stmt)

        except SQLAlchemyError as e:
            logger.exception(
                f"Error was taken on delete"
                f"Error -> {e}"
            )
            raise sql_exeption

            
            
    async def update_one(self, id:int, update_data:dict)->bool:
        try:
            stmt = update(self.model).filter_by(id=id).values(**update_data).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.one_or_none()
        except SQLAlchemyError as e:
            logger.exception(
                f"Error was taken on delete"
                f"Error -> {e}"
            )
            raise sql_exeption


        
        



