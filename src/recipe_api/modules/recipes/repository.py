from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.recipes.model import Recipe


class RecipeRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Recipe]:
        statement = (
            select(Recipe)
            .order_by(Recipe.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id(
        self,
        recipe_id: int,
    ) -> Recipe | None:
        return self.db.get(
            Recipe,
            recipe_id,
        )

    def create(
        self,
        name: str,
        area_id: int,
        category_id: int,
    ) -> Recipe:
        recipe = Recipe(
            name=name,
            area_id=area_id,
            category_id=category_id,
        )

        self.db.add(recipe)
        self.db.flush()
        self.db.refresh(recipe)

        return recipe

    def update(
        self,
        recipe: Recipe,
        name: str,
        area_id: int,
        category_id: int,
    ) -> Recipe:
        recipe.name = name
        recipe.area_id = area_id
        recipe.category_id = category_id

        self.db.flush()
        self.db.refresh(recipe)

        return recipe

    def delete(
        self,
        recipe: Recipe,
    ) -> None:
        self.db.delete(recipe)
        self.db.flush()