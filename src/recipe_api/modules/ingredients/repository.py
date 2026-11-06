from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.ingredients.model import Ingredient


class IngredientRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Ingredient]:
        statement = (
            select(Ingredient)
            .order_by(Ingredient.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id(
        self,
        ingredient_id: int,
    ) -> Ingredient | None:
        return self.db.get(
            Ingredient,
            ingredient_id,
        )

    def create(
        self,
        name: str,
    ) -> Ingredient:
        ingredient = Ingredient(
            name=name
        )

        self.db.add(ingredient)
        self.db.flush()
        self.db.refresh(ingredient)

        return ingredient

    def update(
        self,
        ingredient: Ingredient,
        name: str,
    ) -> Ingredient:
        ingredient.name = name

        self.db.flush()
        self.db.refresh(ingredient)

        return ingredient

    def delete(
        self,
        ingredient: Ingredient,
    ) -> None:
        self.db.delete(ingredient)
        self.db.flush()