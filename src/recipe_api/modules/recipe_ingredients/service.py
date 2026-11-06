from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.modules.ingredients.repository import IngredientRepository
from recipe_api.modules.recipe_ingredients.model import RecipeIngredient
from recipe_api.modules.recipe_ingredients.repository import (
    RecipeIngredientRepository,
)
from recipe_api.modules.recipe_ingredients.schemas import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
)
from recipe_api.modules.recipes.repository import RecipeRepository
from recipe_api.modules.units.repository import UnitRepository


class RecipeIngredientService:

    def __init__(self, db: Session):
        self.db = db

        self.repository = RecipeIngredientRepository(db)
        self.recipe_repository = RecipeRepository(db)
        self.ingredient_repository = IngredientRepository(db)
        self.unit_repository = UnitRepository(db)

    def get_all_by_recipe(
        self,
        recipe_id: int,
    ) -> list[RecipeIngredient]:
        self._validate_recipe(recipe_id)

        return self.repository.find_all_by_recipe(
            recipe_id
        )

    def get_by_id(
        self,
        recipe_id: int,
        recipe_ingredient_id: int,
    ) -> RecipeIngredient:
        self._validate_recipe(recipe_id)

        recipe_ingredient = (
            self.repository.find_by_id_and_recipe(
                recipe_ingredient_id=recipe_ingredient_id,
                recipe_id=recipe_id,
            )
        )

        if recipe_ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente de receta con id "
                f"{recipe_ingredient_id} no existe "
                f"para la receta con id {recipe_id}"
            )

        return recipe_ingredient

    def create(
        self,
        recipe_id: int,
        data: RecipeIngredientCreate,
    ) -> RecipeIngredient:
        self._validate_recipe(recipe_id)
        self._validate_ingredient(data.ingredient_id)
        self._validate_unit(data.unit_id)

        existing_item = (
            self.repository.find_by_recipe_and_item_number(
                recipe_id=recipe_id,
                item_number=data.item_number,
            )
        )

        if existing_item is not None:
            raise ResourceAlreadyExistsError(
                f"El item número {data.item_number} "
                f"ya existe para la receta con id {recipe_id}"
            )

        try:
            recipe_ingredient = self.repository.create(
                recipe_id=recipe_id,
                item_number=data.item_number,
                ingredient_id=data.ingredient_id,
                quantity_text=self._normalize_optional_text(
                    data.quantity_text
                ),
                quantity=data.quantity,
                unit_id=data.unit_id,
                preparation=self._normalize_optional_text(
                    data.preparation
                ),
                original_text=data.original_text.strip(),
            )

            self.db.commit()
            self.db.refresh(recipe_ingredient)

            return recipe_ingredient

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"El item número {data.item_number} "
                f"ya existe para la receta con id {recipe_id}"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        recipe_id: int,
        recipe_ingredient_id: int,
        data: RecipeIngredientUpdate,
    ) -> RecipeIngredient:
        self._validate_recipe(recipe_id)

        recipe_ingredient = (
            self.repository.find_by_id_and_recipe(
                recipe_ingredient_id=recipe_ingredient_id,
                recipe_id=recipe_id,
            )
        )

        if recipe_ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente de receta con id "
                f"{recipe_ingredient_id} no existe "
                f"para la receta con id {recipe_id}"
            )

        self._validate_ingredient(data.ingredient_id)
        self._validate_unit(data.unit_id)

        existing_item = (
            self.repository.find_by_recipe_and_item_number(
                recipe_id=recipe_id,
                item_number=data.item_number,
            )
        )

        if (
            existing_item is not None
            and existing_item.id != recipe_ingredient_id
        ):
            raise ResourceAlreadyExistsError(
                f"El item número {data.item_number} "
                f"ya existe para la receta con id {recipe_id}"
            )

        try:
            updated_recipe_ingredient = self.repository.update(
                recipe_ingredient=recipe_ingredient,
                item_number=data.item_number,
                ingredient_id=data.ingredient_id,
                quantity_text=self._normalize_optional_text(
                    data.quantity_text
                ),
                quantity=data.quantity,
                unit_id=data.unit_id,
                preparation=self._normalize_optional_text(
                    data.preparation
                ),
                original_text=data.original_text.strip(),
            )

            self.db.commit()
            self.db.refresh(updated_recipe_ingredient)

            return updated_recipe_ingredient

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"El item número {data.item_number} "
                f"ya existe para la receta con id {recipe_id}"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        recipe_id: int,
        recipe_ingredient_id: int,
    ) -> None:
        self._validate_recipe(recipe_id)

        recipe_ingredient = (
            self.repository.find_by_id_and_recipe(
                recipe_ingredient_id=recipe_ingredient_id,
                recipe_id=recipe_id,
            )
        )

        if recipe_ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente de receta con id "
                f"{recipe_ingredient_id} no existe "
                f"para la receta con id {recipe_id}"
            )

        try:
            self.repository.delete(
                recipe_ingredient
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def _validate_recipe(
        self,
        recipe_id: int,
    ) -> None:
        recipe = self.recipe_repository.find_by_id(
            recipe_id
        )

        if recipe is None:
            raise ResourceNotFoundError(
                f"La receta con id {recipe_id} no existe"
            )

    def _validate_ingredient(
        self,
        ingredient_id: int,
    ) -> None:
        ingredient = self.ingredient_repository.find_by_id(
            ingredient_id
        )

        if ingredient is None:
            raise ResourceNotFoundError(
                f"El ingrediente con id {ingredient_id} no existe"
            )

    def _validate_unit(
        self,
        unit_id: int | None,
    ) -> None:
        if unit_id is None:
            return

        unit = self.unit_repository.find_by_id(
            unit_id
        )

        if unit is None:
            raise ResourceNotFoundError(
                f"La unidad con id {unit_id} no existe"
            )

    @staticmethod
    def _normalize_optional_text(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized_value = value.strip()

        return normalized_value or None