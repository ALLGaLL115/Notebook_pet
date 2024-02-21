from datetime import datetime
from pydantic import BaseModel

class NotelistCreate(BaseModel):
    title: str
    noteboard_id: int


class NotelistUpdate(NotelistCreate):
    id:int
    

class NotelistRead(NotelistUpdate):

    created_at: datetime
    updated_at: datetime
    notes: list["Note"]