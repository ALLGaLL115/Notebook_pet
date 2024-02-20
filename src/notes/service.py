from sqlalchemy import insert, select, update, delete, exc
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from notes.shemas import NoteBase

from ..models import Note

from ..database import get_async_session



# class NoteUpdate(BaseModel):
#     id: int
#     title: str | None = None
#     notebook_id: int| None = None
#     notelist_id: int| None = None   

class NoteService():

    @staticmethod 
    async def get_note_by_id(note_id: int, db:AsyncSession):
        query = select(Note).filter_by(id = note_id)

        res = await db.execute(query)
        return res.one_or_none()

    @staticmethod
    async def create_note(note: NoteBase, db:AsyncSession):

        stmt = insert(Note).values(note.model_dump())

        await  db.execute(stmt)
        await db.commit()
    
    @staticmethod
    async def get_notes_by_user_id(user_id:int, db:AsyncSession):
        stmt = await select(Note).filter_by(user_id= user_id)


    @staticmethod
    async def update_note_title(note_id: int, new_title: str, db:AsyncSession):
        
        stmt = (
            update(Note)
            .filter_by(id = note_id)
            .values(title=new_title)
        )

        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def update_note_body(note_id: int, new_body: str, db:AsyncSession):
        
        stmt = (
            update(Note)
            .filter_by(id = note_id)
            .values(body = new_body)
        )

        await db.execute(stmt)
        await db.commit()
    
    @staticmethod
    async def delete_note(note_id:int, db:AsyncSession):

        if res.one_or_none() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note with id= {note_id} not found")

        stmt = delete(Note).filter_by(id = note_id)

        await db.execute(stmt)
        await db.commit()
        
    
    


