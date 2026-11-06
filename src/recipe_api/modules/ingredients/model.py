from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from recipe_api.core.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )