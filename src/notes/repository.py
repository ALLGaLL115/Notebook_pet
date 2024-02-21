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

    
    async def get_note_by_id(self, note_id: int, db:AsyncSession):
        query = select(Note).filter_by(id = note_id)

        res = await db.execute(query)
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note with id={note_id} not found")
        return res.one_or_none()

    
    async def create_note(self, note: NoteBase, db:AsyncSession):

        stmt = insert(Note).values(note.model_dump())

        await  db.execute(stmt)
        await db.commit()
    
    
    async def get_notes_by_user_id(self, user_id:int, db:AsyncSession):
        stmt = await select(Note).filter_by(user_id= user_id)

        res = await db.execute(stmt)
        notes = res.scalars().all()
        if not notes:
            raise
        return


    
    async def update_note_title(self, note_id: int, new_title: str, db:AsyncSession):
        
        stmt = (
            update(Note)
            .filter_by(id = note_id)
            .values(title=new_title)
        )

        await db.execute(stmt)
        await db.commit()

    
    async def update_note_body(self, note_id: int, new_body: str, db:AsyncSession):
        
        stmt = (
            update(Note)
            .filter_by(id = note_id)
            .values(body = new_body)
        )

        await db.execute(stmt)
        await db.commit()
    
    
    async def delete_note(self, note_id:int, db:AsyncSession):
        
        await self.get_note_by_id(note_id=note_id, db=db)

        stmt = delete(Note).filter_by(id = note_id)

        await db.execute(stmt)
        await db.commit()
        
    
    


