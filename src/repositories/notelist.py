from models import Notelist
from utils.repository import SQLAlchemyRepository


class NotelistRepository(SQLAlchemyRepository):
    model: Notelist