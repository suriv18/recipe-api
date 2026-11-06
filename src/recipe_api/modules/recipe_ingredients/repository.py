from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.recipe_ingredients.model import RecipeIngredient


class RecipeIngredientRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all_by_recipe(
        self,
        recipe_id: int,
    ) -> list[RecipeIngredient]:
        statement = (
            select(RecipeIngredient)
            .where(RecipeIngredient.recipe_id == recipe_id)
            .order_by(RecipeIngredient.item_number)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id_and_recipe(
        self,
        recipe_ingredient_id: int,
        recipe_id: int,
    ) -> RecipeIngredient | None:
        statement = (
            select(RecipeIngredient)
            .where(
                RecipeIngredient.id == recipe_ingredient_id,
                RecipeIngredient.recipe_id == recipe_id,
            )
        )

        return self.db.scalar(statement)

    def find_by_recipe_and_item_number(
        self,
        recipe_id: int,
        item_number: int,
    ) -> RecipeIngredient | None:
        statement = (
            select(RecipeIngredient)
            .where(
                RecipeIngredient.recipe_id == recipe_id,
                RecipeIngredient.item_number == item_number,
            )
        )

        return self.db.scalar(statement)

    def create(
        self,
        recipe_id: int,
        item_number: int,
        ingredient_id: int,
        quantity_text: str | None,
        quantity: Decimal | None,
        unit_id: int | None,
        preparation: str | None,
        original_text: str,
    ) -> RecipeIngredient:
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            item_number=item_number,
            ingredient_id=ingredient_id,
            quantity_text=quantity_text,
            quantity=quantity,
            unit_id=unit_id,
            preparation=preparation,
            original_text=original_text,
        )

        self.db.add(recipe_ingredient)
        self.db.flush()
        self.db.refresh(recipe_ingredient)

        return recipe_ingredient

    def update(
        self,
        recipe_ingredient: RecipeIngredient,
        item_number: int,
        ingredient_id: int,
        quantity_text: str | None,
        quantity: Decimal | None,
        unit_id: int | None,
        preparation: str | None,
        original_text: str,
    ) -> RecipeIngredient:
        recipe_ingredient.item_number = item_number
        recipe_ingredient.ingredient_id = ingredient_id
        recipe_ingredient.quantity_text = quantity_text
        recipe_ingredient.quantity = quantity
        recipe_ingredient.unit_id = unit_id
        recipe_ingredient.preparation = preparation
        recipe_ingredient.original_text = original_text

        self.db.flush()
        self.db.refresh(recipe_ingredient)

        return recipe_ingredient

    def delete(
        self,
        recipe_ingredient: RecipeIngredient,
    ) -> None:
        self.db.delete(recipe_ingredient)
        self.db.flush()