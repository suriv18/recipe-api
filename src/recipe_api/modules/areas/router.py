from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from recipe_api.common.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from recipe_api.core.database import get_db
from recipe_api.modules.areas.schemas import (
    AreaCreate,
    AreaResponse,
    AreaUpdate,
)
from recipe_api.modules.areas.service import AreaService


router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
)


@router.get(
    "",
    response_model=list[AreaResponse],
    status_code=status.HTTP_200_OK,
)
def get_areas(
    db: Annotated[Session, Depends(get_db)],
) -> list[AreaResponse]:
    service = AreaService(db)

    return service.get_all()


@router.get(
    "/{area_id}",
    response_model=AreaResponse,
    status_code=status.HTTP_200_OK,
)
def get_area_by_id(
    area_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> AreaResponse:
    service = AreaService(db)

    try:
        return service.get_by_id(area_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=AreaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_area(
    data: AreaCreate,
    db: Annotated[Session, Depends(get_db)],
) -> AreaResponse:
    service = AreaService(db)

    try:
        return service.create(data)

    except ResourceAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{area_id}",
    response_model=AreaResponse,
    status_code=status.HTTP_200_OK,
)
def update_area(
    area_id: Annotated[int, Path(gt=0)],
    data: AreaUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> AreaResponse:
    service = AreaService(db)

    try:
        return service.update(
            area_id=area_id,
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
    "/{area_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_area(
    area_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = AreaService(db)

    try:
        service.delete(area_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error