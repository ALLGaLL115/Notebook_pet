
from sqlalchemy import text, Table, Column, MetaData, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from typing import Annotated
import datetime



intPk = Annotated[int, mapped_column(primary_key=True)]
nonnull_str = Annotated[str, mapped_column(nullable=False)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.now(datetime.UTC))]




