from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.areas.model import Area


class AreaRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Area]:
        statement = (
            select(Area)
            .order_by(Area.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id(self, area_id: int) -> Area | None:
        return self.db.get(Area, area_id)

    def find_by_name(self, name: str) -> Area | None:
        statement = (
            select(Area)
            .where(Area.name == name)
        )

        return self.db.scalar(statement)

    def create(self, name: str) -> Area:
        area = Area(
            name=name
        )

        self.db.add(area)
        self.db.flush()
        self.db.refresh(area)

        return area

    def update(self, area: Area, name: str) -> Area:
        area.name = name

        self.db.flush()
        self.db.refresh(area)

        return area

    def delete(self, area: Area) -> None:
        self.db.delete(area)
        self.db.flush()