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
from recipe_api.modules.units.schemas import (
    UnitCreate,
    UnitResponse,
    UnitUpdate,
)
from recipe_api.modules.units.service import UnitService


router = APIRouter(
    prefix="/units",
    tags=["Units"],
)


@router.get(
    "",
    response_model=list[UnitResponse],
    status_code=status.HTTP_200_OK,
)
def get_units(
    db: Annotated[Session, Depends(get_db)],
) -> list[UnitResponse]:
    service = UnitService(db)

    return service.get_all()


@router.get(
    "/{unit_id}",
    response_model=UnitResponse,
    status_code=status.HTTP_200_OK,
)
def get_unit_by_id(
    unit_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> UnitResponse:
    service = UnitService(db)

    try:
        return service.get_by_id(unit_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=UnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_unit(
    data: UnitCreate,
    db: Annotated[Session, Depends(get_db)],
) -> UnitResponse:
    service = UnitService(db)

    try:
        return service.create(data)

    except ResourceAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{unit_id}",
    response_model=UnitResponse,
    status_code=status.HTTP_200_OK,
)
def update_unit(
    unit_id: Annotated[int, Path(gt=0)],
    data: UnitUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> UnitResponse:
    service = UnitService(db)

    try:
        return service.update(
            unit_id=unit_id,
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
    "/{unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_unit(
    unit_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = UnitService(db)

    try:
        service.delete(unit_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error