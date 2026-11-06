from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from recipe_api.core.database import Base


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )