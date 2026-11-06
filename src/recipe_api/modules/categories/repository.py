from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.categories.model import Category


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Category]:
        statement = (
            select(Category)
            .order_by(Category.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id(
        self,
        category_id: int,
    ) -> Category | None:
        return self.db.get(
            Category,
            category_id,
        )

    def find_by_name(
        self,
        name: str,
    ) -> Category | None:
        statement = (
            select(Category)
            .where(Category.name == name)
        )

        return self.db.scalar(statement)

    def create(
        self,
        name: str,
    ) -> Category:
        category = Category(
            name=name
        )

        self.db.add(category)
        self.db.flush()
        self.db.refresh(category)

        return category

    def update(
        self,
        category: Category,
        name: str,
    ) -> Category:
        category.name = name

        self.db.flush()
        self.db.refresh(category)

        return category

    def delete(
        self,
        category: Category,
    ) -> None:
        self.db.delete(category)
        self.db.flush()