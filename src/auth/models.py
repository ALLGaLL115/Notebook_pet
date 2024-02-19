from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column

class UserTable(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    # email:Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)