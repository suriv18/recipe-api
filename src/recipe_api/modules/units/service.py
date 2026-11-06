from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.modules.units.model import Unit
from recipe_api.modules.units.repository import UnitRepository
from recipe_api.modules.units.schemas import (
    UnitCreate,
    UnitUpdate,
)


class UnitService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UnitRepository(db)

    def get_all(self) -> list[Unit]:
        return self.repository.find_all()

    def get_by_id(
        self,
        unit_id: int,
    ) -> Unit:
        unit = self.repository.find_by_id(unit_id)

        if unit is None:
            raise ResourceNotFoundError(
                f"La unidad con id {unit_id} no existe"
            )

        return unit

    def create(
        self,
        data: UnitCreate,
    ) -> Unit:
        name = data.name.strip()

        existing_unit = self.repository.find_by_name(name)

        if existing_unit is not None:
            raise ResourceAlreadyExistsError(
                f"La unidad '{name}' ya existe"
            )

        try:
            unit = self.repository.create(name)

            self.db.commit()
            self.db.refresh(unit)

            return unit

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"La unidad '{name}' ya existe"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        unit_id: int,
        data: UnitUpdate,
    ) -> Unit:
        unit = self.repository.find_by_id(unit_id)

        if unit is None:
            raise ResourceNotFoundError(
                f"La unidad con id {unit_id} no existe"
            )

        name = data.name.strip()

        existing_unit = self.repository.find_by_name(name)

        if (
            existing_unit is not None
            and existing_unit.id != unit_id
        ):
            raise ResourceAlreadyExistsError(
                f"La unidad '{name}' ya existe"
            )

        try:
            updated_unit = self.repository.update(
                unit=unit,
                name=name,
            )

            self.db.commit()
            self.db.refresh(updated_unit)

            return updated_unit

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"La unidad '{name}' ya existe"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        unit_id: int,
    ) -> None:
        unit = self.repository.find_by_id(unit_id)

        if unit is None:
            raise ResourceNotFoundError(
                f"La unidad con id {unit_id} no existe"
            )

        try:
            self.repository.delete(unit)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise