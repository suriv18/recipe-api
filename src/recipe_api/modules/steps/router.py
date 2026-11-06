from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Response,
    status,
)
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.core.database import get_db
from recipe_api.modules.steps.schemas import (
    StepCreate,
    StepResponse,
    StepUpdate,
)
from recipe_api.modules.steps.service import StepService


router = APIRouter(
    prefix="/recipes/{recipe_id}/steps",
    tags=["Steps"],
)


@router.get(
    "",
    response_model=list[StepResponse],
    status_code=status.HTTP_200_OK,
)
def get_steps_by_recipe(
    recipe_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> list[StepResponse]:
    service = StepService(db)

    try:
        return service.get_all_by_recipe(recipe_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/{step_id}",
    response_model=StepResponse,
    status_code=status.HTTP_200_OK,
)
def get_step_by_id(
    recipe_id: Annotated[int, Path(gt=0)],
    step_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> StepResponse:
    service = StepService(db)

    try:
        return service.get_by_id(
            recipe_id=recipe_id,
            step_id=step_id,
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=StepResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_step(
    recipe_id: Annotated[int, Path(gt=0)],
    data: StepCreate,
    db: Annotated[Session, Depends(get_db)],
) -> StepResponse:
    service = StepService(db)

    try:
        return service.create(
            recipe_id=recipe_id,
            data=data,
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except ResourceAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{step_id}",
    response_model=StepResponse,
    status_code=status.HTTP_200_OK,
)
def update_step(
    recipe_id: Annotated[int, Path(gt=0)],
    step_id: Annotated[int, Path(gt=0)],
    data: StepUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> StepResponse:
    service = StepService(db)

    try:
        return service.update(
            recipe_id=recipe_id,
            step_id=step_id,
            data=data,
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except ResourceAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{step_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_step(
    recipe_id: Annotated[int, Path(gt=0)],
    step_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = StepService(db)

    try:
        service.delete(
            recipe_id=recipe_id,
            step_id=step_id,
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error