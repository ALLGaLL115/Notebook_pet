from datetime import datetime
from pydantic import BaseModel


class NotebookShcema(BaseModel):
  id:int 
  title:int 
  user_id:int 
  created_at:datetime 
  updated_at:datetime 

class NotebookCreate(BaseModel):
  title: str
  user_id: int



class NotebookWithNotes(NotebookShcema):
  notes: list["Note"]
