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
from recipe_api.modules.categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from recipe_api.modules.categories.service import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    "",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_categories(
    db: Annotated[Session, Depends(get_db)],
) -> list[CategoryResponse]:
    service = CategoryService(db)

    return service.get_all()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_category_by_id(
    category_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> CategoryResponse:
    service = CategoryService(db)

    try:
        return service.get_by_id(category_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    db: Annotated[Session, Depends(get_db)],
) -> CategoryResponse:
    service = CategoryService(db)

    try:
        return service.create(data)

    except ResourceAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
def update_category(
    category_id: Annotated[int, Path(gt=0)],
    data: CategoryUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> CategoryResponse:
    service = CategoryService(db)

    try:
        return service.update(
            category_id=category_id,
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
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = CategoryService(db)

    try:
        service.delete(category_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error