from sqlalchemy import insert, select, update, delete, exc
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from ..models import Notelist

from ..database import get_async_session 

from .shemas import NotelistUpdate, NotelistCreate, NotelistRead




class NotelistRepository():

    async def create_notelist(self, new_notelist: NotelistCreate, db:AsyncSession):
        stmt = insert(Notelist).values(new_notelist).returning()

        try:
            await db.execute(stmt)
            await db.commit()
        except exc.SQLAlchemyError:
            
            raise HTTPException(status_code=500, detail="Internal server error")
           
    
    async def get_notelist_by_id(self, notelist_id:int, db:AsyncSession) -> Notelist |None:
         query = select(Notelist).filter_by(id = notelist_id)

         res = await db.execute(query)

         notelist_db = res.scalar_one_or_none()
         return notelist_db

    async def delete_notelist(self, notelist_id:int, db:AsyncSession):
        notelist_db = await self.get_notelist_by_id(notelist_id, db)

        if notelist_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Notelist with id={notelist_id} not found")

        stmt = delete(Notelist).filter_by(id = notelist_id)

        try :
            await db.execute(stmt)
            await db.commit()
        except exc.SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on server side")

    async def update_notelist():
        pass #Changes related to notelists