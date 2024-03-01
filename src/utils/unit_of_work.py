from abc import ABC, abstractclassmethod
from typing import Annotated, Type
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from database import async_session_maker
from repositories.assotiations.note_notebook import AssotiationNoteNotebookRepository
from repositories.note import NoteRepository
from repositories.noteboard import NoteboardRepository
from repositories.notebook import NotebookRepository
from repositories.notelist import NotelistRepository
from repositories.user import UserRepository


class IUnitOfWork(ABC):
    users:Type[UserRepository]
    notes:Type[NoteRepository]
    notebooks:Type[NotebookRepository]
    notelists:Type[NotelistRepository]
    noteboards:Type[NoteboardRepository]

    assotiations_notebook_note: Type[AssotiationNoteNotebookRepository]
    
    def __init__(self):
        raise NotImplementedError

        
    
    @abstractclassmethod
    def __aenter__(self):
        raise NotImplementedError    
    @abstractclassmethod
    def __aexit__(self, *args):
        raise NotImplementedError    
    @abstractclassmethod
    def rollback(self):
        raise NotImplementedError    
    @abstractclassmethod
    def commit(self):
        raise NotImplementedError
    

class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.notes = NoteRepository(self.session)
        self.notebooks = NotebookRepository(self.session)
        self.notelists = NotelistRepository(self.session)
        self.noteboards = NoteboardRepository(self.session)

        return self
    
    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()
      
    async def commit(self):
        await self.session.commit()
        




