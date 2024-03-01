import datetime
from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import VARCHAR, ForeignKey, text


intPk = Annotated[int, mapped_column(primary_key=True)]
nonnull_str = Annotated[str, mapped_column(nullable=False)]
title_256 = Annotated[str, mapped_column(type_=VARCHAR(256))]

user_fk = Annotated[int, mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.now(datetime.UTC))]