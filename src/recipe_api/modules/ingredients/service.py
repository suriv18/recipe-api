from sqlalchemy.orm import Session

from recipe_api.common.exceptions import ResourceNotFoundError
from recipe_api.modules.ingredients.model import Ingredient
from recipe_api.modules.ingredients.repository import IngredientRepository
from recipe_api.modules.ingredients.schemas import (
    IngredientCreate,
    IngredientUpdate,
)


class IngredientService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = IngredientRepository(db)

    def get_all(self) -> list[Ingredient]:
        return self.repository.find_all()

    def get_by_id(
        self,
        ingredient_id: int,
    ) -> Ingredient:
        ingredient = self.repository.find_by_id(
            ingredient_id
        )

        if ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente con id {ingredient_id} no existe"
            )

        return ingredient

    def create(
        self,
        data: IngredientCreate,
    ) -> Ingredient:
        name = data.name.strip()

        try:
            ingredient = self.repository.create(
                name=name
            )

            self.db.commit()
            self.db.refresh(ingredient)

            return ingredient

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        ingredient_id: int,
        data: IngredientUpdate,
    ) -> Ingredient:
        ingredient = self.repository.find_by_id(
            ingredient_id
        )

        if ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente con id {ingredient_id} no existe"
            )

        name = data.name.strip()

        try:
            updated_ingredient = self.repository.update(
                ingredient=ingredient,
                name=name,
            )

            self.db.commit()
            self.db.refresh(updated_ingredient)

            return updated_ingredient

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        ingredient_id: int,
    ) -> None:
        ingredient = self.repository.find_by_id(
            ingredient_id
        )

        if ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente con id {ingredient_id} no existe"
            )

        try:
            self.repository.delete(ingredient)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise