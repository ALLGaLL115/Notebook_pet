from pydantic import BaseModel
from datetime import datetime
class NoteBase(BaseModel):
    body: str | None = None
    title: str | None = None
    user_id: int
    notelist_id: int| None = None

class NoteCreate(BaseModel):
    body: str|None =None
    title: str|None =None


class NoteRead(NoteBase):
    id: int

    created_at: datetime
    updated_at: datetime
