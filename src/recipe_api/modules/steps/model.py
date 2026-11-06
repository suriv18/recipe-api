from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    SmallInteger,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from recipe_api.core.database import Base


class Step(Base):
    __tablename__ = "steps"

    __table_args__ = (
        CheckConstraint(
            "step_number > 0",
            name="ck_steps_step_number_positive",
        ),
        UniqueConstraint(
            "recipe_id",
            "step_number",
            name="uq_steps_recipe_step_number",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
    )

    recipe_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "recipes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    step_number: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )