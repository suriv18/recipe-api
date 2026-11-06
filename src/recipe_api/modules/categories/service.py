from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.modules.categories.model import Category
from recipe_api.modules.categories.repository import CategoryRepository
from recipe_api.modules.categories.schemas import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def get_all(self) -> list[Category]:
        return self.repository.find_all()

    def get_by_id(
        self,
        category_id: int,
    ) -> Category:
        category = self.repository.find_by_id(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                f"La categoría con id {category_id} no existe"
            )

        return category

    def create(
        self,
        data: CategoryCreate,
    ) -> Category:
        name = data.name.strip()

        existing_category = self.repository.find_by_name(
            name
        )

        if existing_category is not None:
            raise ResourceAlreadyExistsError(
                f"La categoría '{name}' ya existe"
            )

        try:
            category = self.repository.create(
                name
            )

            self.db.commit()
            self.db.refresh(category)

            return category

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"La categoría '{name}' ya existe"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Category:
        category = self.repository.find_by_id(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                f"La categoría con id {category_id} no existe"
            )

        name = data.name.strip()

        existing_category = self.repository.find_by_name(
            name
        )

        if (
            existing_category is not None
            and existing_category.id != category_id
        ):
            raise ResourceAlreadyExistsError(
                f"La categoría '{name}' ya existe"
            )

        try:
            updated_category = self.repository.update(
                category=category,
                name=name,
            )

            self.db.commit()
            self.db.refresh(updated_category)

            return updated_category

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"La categoría '{name}' ya existe"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        category_id: int,
    ) -> None:
        category = self.repository.find_by_id(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                f"La categoría con id {category_id} no existe"
            )

        try:
            self.repository.delete(category)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise