from models import Notebook
from utils.repository import SQLAlchemyRepository


class NotebookRepository(SQLAlchemyRepository):
    model: Notebook