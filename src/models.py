
import datetime
from typing import Annotated
from sqlalchemy import ForeignKey, text, Table, Column, MetaData, Integer, String, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
# from models.utils import intPk, nonnull_str, user_fk, created_at, updated_at, title_256
from shemas.user import UserShema


intPk = Annotated[int, mapped_column(primary_key=True)]
nonnull_str = Annotated[str, mapped_column(nullable=False)]
title_256 = Annotated[str, mapped_column(type_=VARCHAR(256))]

user_fk = Annotated[int, mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.now(datetime.UTC))]


class User(Base):
  __tablename__ = "users"
  id : Mapped[intPk]
  email: Mapped[str] = mapped_column(unique=True, nullable= False)
  username : Mapped[nonnull_str]
  hashed_password: Mapped[nonnull_str]
  created_at : Mapped[created_at]

  notes: Mapped[list["Note"]] = relationship(
    "Note",
    back_populates= "user"
  )
  notebooks: Mapped[list["Notebook"]] = relationship(
    "Notebook",
    back_populates= "user"
  )
  noteboards: Mapped[list["Noteboard"]] = relationship(
    "Noteboard",
    back_populates= "user"
  )

  def convert_to_model(self):
    return UserShema(
      id = self.id,
      email = self.email,
      username = self.username,
      hashed_password = self.hashed_password,
      created_at = self.created_at
    )
    
 
class Note (Base):
  __tablename__ = "notes" 
  id: Mapped[intPk]
  title: Mapped[title_256] = mapped_column(nullable=True)
  body: Mapped[str] = mapped_column(nullable=True)
  # notelist_id: Mapped[int] = mapped_column(ForeignKey("notelists.id", ondelete="CASCADE"), nullable=True, default=None)
  created_at: Mapped[created_at]
  updated_at: Mapped[updated_at]
  
  user: Mapped["User"] = relationship(
    "User",
    back_populates = "notes"
  )
  notebooks: Mapped[list["Notebook"]] = relationship(
    "Notebook",
    back_populates = "notes",
    secondary="assotiation_note_notebook"
  )
  notelist: Mapped["Notelist"] = relationship(
    "Notelist",
    back_populates = "notes"
  )


class Notebook (Base):
  __tablename__ = "notebooks" 
  id: Mapped[intPk]
  title: Mapped[str]
  user_id: Mapped[user_fk]
  created_at: Mapped[created_at]
  updated_at: Mapped[updated_at]

  user: Mapped["User"] = relationship(
    "User",
    back_populates="notebooks"
  )

  notes: Mapped[list["Note"]] = relationship(
    "Note",
    back_populates="notebooks",
    secondary="assotiation_note_notebook"

  )


class AssotiationUserNotebook(Base):
  __tablename__="assotiation_user_notebook"
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  note_id: Mapped[int] = mapped_column(ForeignKey("notebooks.id", ondelete="CASCADE"), primary_key=True)


class AssotiationNoteNotebook(Base):
  __tablename__ = "assotiation_note_notebook"
  notebook_id: Mapped[int] = mapped_column(ForeignKey("notebooks.id", ondelete="CASCADE"), primary_key=True)
  note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)



class Notelist (Base):
  __tablename__ = "notelists" 
  id: Mapped[intPk]
  title: Mapped[title_256]
  noteboard_id: Mapped[int] = mapped_column(ForeignKey("noteboards.id"))
  created_at: Mapped[created_at]
  updated_at: Mapped[updated_at]
  
  noteboard: Mapped["Noteboard"] = relationship(
    "Noteboard",
    back_populates="notelists"
  )
  notes: Mapped[list[Note]] = relationship(
    "Note",
    back_populates="notelist"
  )



class Noteboard (Base):
  __tablename__ = "noteboards" 
  id: Mapped[intPk]
  title: Mapped[title_256]
  user_id: Mapped[user_fk]
  created_at: Mapped[created_at]
  updated_at: Mapped[updated_at]

  user: Mapped["User"] = relationship(
    "User",
    back_populates="noteboards"
  )
  notelists: Mapped[list[Notelist]] = relationship(
    "Notelist",
    back_populates="noteboard"
  )

