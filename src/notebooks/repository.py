from sqlalchemy import insert, select, update, delete, exc
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from notes.shemas import NoteRead

from ..models import Notebook

from ..database import get_async_session


from pydantic import BaseModel
from datetime import datetime
class NotebookBase(BaseModel):
    title: str|None = None
    user_id: int

class NotebookRead(BaseModel):

    id: int
    notes: int
    created_at: datetime
    

    # body: str | None = None
    # title: str | None = None
    # user_id: int
    # notebook_id: int
    # notelist_id: int| None = None

class NotebookWithNotes(NotebookBase):
    id: int
    notes: list["NoteRead"]
    created_at: datetime
    updated_at: datetime




class NotebookService():

    
    async def get_notebook_by_id(self, notebook_id:int, db:AsyncSession): 
        query = select(Notebook).filter_by(id = notebook_id)

        res = await db.execute(query)
        notebook_db = res.one_or_none()
        # if notebook_db is None:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note with id= {note_id} not found")
        return notebook_db


    
    async def create_notebook(self, new_notebook: NotebookBase, db:AsyncSession):
        stmt = insert(Notebook).values(title= new_notebook.title, user_id = new_notebook.user_id)

        await db.execute(stmt)
        await db.commit()
    
    
    async def change_title(self, notebook_id:int, new_title:str, db: AsyncSession):
        stmt = update(Notebook).filter_by(id = notebook_id).values(title = new_title)

        await db.execute(stmt)
        await db.commit()

    
    async def delete_notebook_by_id(self, notebook_id:int, db:AsyncSession):
        notebook_db = await self.get_notebook_by_id
        if notebook_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note with id= {note_id} not found")

        stmt = delete(Notebook).filter_by(id = notebook_id)
        try:
            await db.execute(stmt)
            await db.commit()
        except exc.SQLAlchemyError:
            
            raise HTTPException(status_code=500, detail="Internal server error")
        
