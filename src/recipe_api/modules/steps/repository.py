from sqlalchemy import select
from sqlalchemy.orm import Session

from recipe_api.modules.steps.model import Step


class StepRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all_by_recipe(
        self,
        recipe_id: int,
    ) -> list[Step]:
        statement = (
            select(Step)
            .where(Step.recipe_id == recipe_id)
            .order_by(Step.step_number)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def find_by_id_and_recipe(
        self,
        step_id: int,
        recipe_id: int,
    ) -> Step | None:
        statement = (
            select(Step)
            .where(
                Step.id == step_id,
                Step.recipe_id == recipe_id,
            )
        )

        return self.db.scalar(statement)

    def find_by_recipe_and_step_number(
        self,
        recipe_id: int,
        step_number: int,
    ) -> Step | None:
        statement = (
            select(Step)
            .where(
                Step.recipe_id == recipe_id,
                Step.step_number == step_number,
            )
        )

        return self.db.scalar(statement)

    def create(
        self,
        recipe_id: int,
        step_number: int,
        description: str,
    ) -> Step:
        step = Step(
            recipe_id=recipe_id,
            step_number=step_number,
            description=description,
        )

        self.db.add(step)
        self.db.flush()
        self.db.refresh(step)

        return step

    def update(
        self,
        step: Step,
        step_number: int,
        description: str,
    ) -> Step:
        step.step_number = step_number
        step.description = description

        self.db.flush()
        self.db.refresh(step)

        return step

    def delete(
        self,
        step: Step,
    ) -> None:
        self.db.delete(step)
        self.db.flush()