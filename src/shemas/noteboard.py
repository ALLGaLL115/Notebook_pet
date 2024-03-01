from datetime import datetime

from pydantic import BaseModel









class NoteboardSchema(BaseModel):
  id: int
  title: str
  user_id: int
  created_at: datetime
  updated_at: datetime

class NoteboardCreate(BaseModel):
  title: str
  user_id: int

class NoteboardWithNoteLists(NoteboardSchema):
  notelists: list["NotelistSchema"]









