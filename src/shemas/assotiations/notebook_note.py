from pydantic import BaseModel


class AssotiationNoteNotebookSchema(BaseModel):
  notebook_id: int
  note_id: int

