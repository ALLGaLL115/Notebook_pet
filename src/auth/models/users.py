from sqlalchemy import text, Table, Column, MetaData, Integer,Boolean, String, sql, DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("username", String),
    Column("hashed_password", String),
    Column("is_active", Boolean(),
           server_default=sql.expression.true(),
           nullable=False)
)

tokens_table = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "token",
        UUID(as_uuid=False),
        server_default=text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True
    ),
    Column("expires", DateTime()),
    Column("user_id", ForeignKey(user_table.c.id))
)





