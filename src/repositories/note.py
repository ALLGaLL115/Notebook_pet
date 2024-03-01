from models import Note
from utils.repository import SQLAlchemyRepository


class NoteRepository(SQLAlchemyRepository):
    model: Note