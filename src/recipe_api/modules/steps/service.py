from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.modules.recipes.repository import RecipeRepository
from recipe_api.modules.steps.model import Step
from recipe_api.modules.steps.repository import StepRepository
from recipe_api.modules.steps.schemas import (
    StepCreate,
    StepUpdate,
)


class StepService:

    def __init__(self, db: Session):
        self.db = db

        self.repository = StepRepository(db)
        self.recipe_repository = RecipeRepository(db)

    def get_all_by_recipe(
        self,
        recipe_id: int,
    ) -> list[Step]:
        self._validate_recipe(recipe_id)

        return self.repository.find_all_by_recipe(
            recipe_id
        )

    def get_by_id(
        self,
        recipe_id: int,
        step_id: int,
    ) -> Step:
        self._validate_recipe(recipe_id)

        step = self.repository.find_by_id_and_recipe(
            step_id=step_id,
            recipe_id=recipe_id,
        )

        if step is None:
            raise ResourceNotFoundError(
                f"El paso con id {step_id} no existe "
                f"para la receta con id {recipe_id}"
            )

        return step

    def create(
        self,
        recipe_id: int,
        data: StepCreate,
    ) -> Step:
        self._validate_recipe(recipe_id)

        description = data.description.strip()

        existing_step = (
            self.repository.find_by_recipe_and_step_number(
                recipe_id=recipe_id,
                step_number=data.step_number,
            )
        )

        if existing_step is not None:
            raise ResourceAlreadyExistsError(
                f"El paso número {data.step_number} "
                f"ya existe para la receta con id {recipe_id}"
            )

        try:
            step = self.repository.create(
                recipe_id=recipe_id,
                step_number=data.step_number,
                description=description,
            )

            self.db.commit()
            self.db.refresh(step)

            return step

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"El paso número {data.step_number} "
                f"ya existe para la receta con id {recipe_id}"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def update(
        self,
        recipe_id: int,
        step_id: int,
        data: StepUpdate,
    ) -> Step:
        self._validate_recipe(recipe_id)

        step = self.repository.find_by_id_and_recipe(
            step_id=step_id,
            recipe_id=recipe_id,
        )

        if step is None:
            raise ResourceNotFoundError(
                f"El paso con id {step_id} no existe "
                f"para la receta con id {recipe_id}"
            )

        description = data.description.strip()

        existing_step = (
            self.repository.find_by_recipe_and_step_number(
                recipe_id=recipe_id,
                step_number=data.step_number,
            )
        )

        if (
            existing_step is not None
            and existing_step.id != step_id
        ):
            raise ResourceAlreadyExistsError(
                f"El paso número {data.step_number} "
                f"ya existe para la receta con id {recipe_id}"
            )

        try:
            updated_step = self.repository.update(
                step=step,
                step_number=data.step_number,
                description=description,
            )

            self.db.commit()
            self.db.refresh(updated_step)

            return updated_step

        except IntegrityError as error:
            self.db.rollback()

            raise ResourceAlreadyExistsError(
                f"El paso número {data.step_number} "
                f"ya existe para la receta con id {recipe_id}"
            ) from error

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        recipe_id: int,
        step_id: int,
    ) -> None:
        self._validate_recipe(recipe_id)

        step = self.repository.find_by_id_and_recipe(
            step_id=step_id,
            recipe_id=recipe_id,
        )

        if step is None:
            raise ResourceNotFoundError(
                f"El paso con id {step_id} no existe "
                f"para la receta con id {recipe_id}"
            )

        try:
            self.repository.delete(step)

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