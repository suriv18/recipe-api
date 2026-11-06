from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.modules.areas.model import Area
from recipe_api.modules.areas.repository import AreaRepository
from recipe_api.modules.areas.schemas import AreaCreate, AreaUpdate


class AreaService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = AreaRepository(db)

    def get_all(self) -> list[Area]:
        return self.repository.find_all()

    def get_by_id(self, area_id: int) -> Area:
        area = self.repository.find_by_id(area_id)

        if area is None:
            raise ResourceNotFoundError(
                f"El área con id {area_id} no existe"
            )

        return area

    def create(self, data: AreaCreate) -> Area:
        name = data.name.strip()

        existing_area = self.repository.find_by_name(name)

        if existing_area is not None:
            raise ResourceAlreadyExistsError(
                f"El área '{name}' ya existe"
            )

        try:
            area = self.repository.create(name)

            self.db.commit()
            self.db.refresh(area)

            return area

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"El área '{name}' ya existe"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        area_id: int,
        data: AreaUpdate,
    ) -> Area:

        area = self.repository.find_by_id(area_id)

        if area is None:
            raise ResourceNotFoundError(
                f"El área con id {area_id} no existe"
            )

        name = data.name.strip()

        existing_area = self.repository.find_by_name(name)

        if (
            existing_area is not None
            and existing_area.id != area_id
        ):
            raise ResourceAlreadyExistsError(
                f"El área '{name}' ya existe"
            )

        try:
            updated_area = self.repository.update(
                area=area,
                name=name,
            )

            self.db.commit()
            self.db.refresh(updated_area)

            return updated_area

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"El área '{name}' ya existe"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def delete(self, area_id: int) -> None:
        area = self.repository.find_by_id(area_id)

        if area is None:
            raise ResourceNotFoundError(
                f"El área con id {area_id} no existe"
            )

        try:
            self.repository.delete(area)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise