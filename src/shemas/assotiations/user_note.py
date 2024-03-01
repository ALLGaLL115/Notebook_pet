
from pydantic import BaseModel


class AssotiationUserNotebook(BaseModel):
    user_id: int
    notebook_id: int