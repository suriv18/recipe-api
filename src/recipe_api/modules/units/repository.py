from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.units.model import Unit


class UnitRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Unit]:
        statement = (
            select(Unit)
            .order_by(Unit.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id(
        self,
        unit_id: int,
    ) -> Unit | None:
        return self.db.get(
            Unit,
            unit_id,
        )

    def find_by_name(
        self,
        name: str,
    ) -> Unit | None:
        statement = (
            select(Unit)
            .where(Unit.name == name)
        )

        return self.db.scalar(statement)

    def create(
        self,
        name: str,
    ) -> Unit:
        unit = Unit(
            name=name
        )

        self.db.add(unit)
        self.db.flush()
        self.db.refresh(unit)

        return unit

    def update(
        self,
        unit: Unit,
        name: str,
    ) -> Unit:
        unit.name = name

        self.db.flush()
        self.db.refresh(unit)

        return unit

    def delete(
        self,
        unit: Unit,
    ) -> None:
        self.db.delete(unit)
        self.db.flush()