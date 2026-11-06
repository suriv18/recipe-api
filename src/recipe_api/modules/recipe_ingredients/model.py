from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from recipe_api.core.database import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    __table_args__ = (
        CheckConstraint(
            "item_number > 0",
            name="ck_recipe_ingredients_item_number_positive",
        ),
        UniqueConstraint(
            "recipe_id",
            "item_number",
            name="uq_recipe_ingredients_recipe_item_number",
        ),
        Index(
            "ix_recipe_ingredients_ingredient",
            "ingredient_id",
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

    item_number: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    ingredient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False,
    )

    quantity_text: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    quantity: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 3),
        nullable=True,
    )

    unit_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("units.id"),
        nullable=True,
    )

    preparation: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    original_text: Mapped[str] = mapped_column(
        String(400),
        nullable=False,
    )