from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import ResourceNotFoundError
from recipe_api.modules.areas.repository import AreaRepository
from recipe_api.modules.categories.repository import CategoryRepository
from recipe_api.modules.recipes.model import Recipe
from recipe_api.modules.recipes.repository import RecipeRepository
from recipe_api.modules.recipes.schemas import (
    RecipeCreate,
    RecipeUpdate,
)


class RecipeService:

    def __init__(self, db: Session):
        self.db = db

        self.repository = RecipeRepository(db)
        self.area_repository = AreaRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all(self) -> list[Recipe]:
        return self.repository.find_all()

    def get_by_id(
        self,
        recipe_id: int,
    ) -> Recipe:
        recipe = self.repository.find_by_id(recipe_id)

        if recipe is None:
            raise ResourceNotFoundError(
                f"La receta con id {recipe_id} no existe"
            )

        return recipe

    def create(
        self,
        data: RecipeCreate,
    ) -> Recipe:
        name = data.name.strip()

        self._validate_area(data.area_id)
        self._validate_category(data.category_id)

        try:
            recipe = self.repository.create(
                name=name,
                area_id=data.area_id,
                category_id=data.category_id,
            )

            self.db.commit()
            self.db.refresh(recipe)

            return recipe

        except IntegrityError:
            self.db.rollback()
            raise

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        recipe_id: int,
        data: RecipeUpdate,
    ) -> Recipe:
        recipe = self.repository.find_by_id(recipe_id)

        if recipe is None:
            raise ResourceNotFoundError(
                f"La receta con id {recipe_id} no existe"
            )

        name = data.name.strip()

        self._validate_area(data.area_id)
        self._validate_category(data.category_id)

        try:
            updated_recipe = self.repository.update(
                recipe=recipe,
                name=name,
                area_id=data.area_id,
                category_id=data.category_id,
            )

            self.db.commit()
            self.db.refresh(updated_recipe)

            return updated_recipe

        except IntegrityError:
            self.db.rollback()
            raise

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        recipe_id: int,
    ) -> None:
        recipe = self.repository.find_by_id(recipe_id)

        if recipe is None:
            raise ResourceNotFoundError(
                f"La receta con id {recipe_id} no existe"
            )

        try:
            self.repository.delete(recipe)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def _validate_area(
        self,
        area_id: int,
    ) -> None:
        area = self.area_repository.find_by_id(area_id)

        if area is None:
            raise ResourceNotFoundError(
                f"El área con id {area_id} no existe"
            )

    def _validate_category(
        self,
        category_id: int,
    ) -> None:
        category = self.category_repository.find_by_id(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                f"La categoría con id {category_id} no existe"
            )