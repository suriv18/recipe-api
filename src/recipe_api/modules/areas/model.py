from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from recipe_api.core.database import Base


class Area(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )