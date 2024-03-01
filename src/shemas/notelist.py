from datetime import datetime
from pydantic import BaseModel

class NotelistCreate(BaseModel):
    title: str
    noteboard_id: int


class NotelistShema(NotelistCreate):
    id: int 
    title: int 
    noteboard_id: int 
    created_at: datetime 
    updated_at: datetime 
    

class NotelistWithNotes(NotelistShema):
  notes: list["Note"]

