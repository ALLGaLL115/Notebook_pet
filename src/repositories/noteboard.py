from models import Noteboard
from utils.repository import SQLAlchemyRepository


class NoteboardRepository(SQLAlchemyRepository):
    model: Noteboard