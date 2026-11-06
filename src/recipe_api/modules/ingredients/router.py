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

from recipe_api.common.exceptions import ResourceNotFoundError
from recipe_api.core.database import get_db
from recipe_api.modules.ingredients.schemas import (
    IngredientCreate,
    IngredientResponse,
    IngredientUpdate,
)
from recipe_api.modules.ingredients.service import IngredientService


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
)


@router.get(
    "",
    response_model=list[IngredientResponse],
    status_code=status.HTTP_200_OK,
)
def get_ingredients(
    db: Annotated[Session, Depends(get_db)],
) -> list[IngredientResponse]:
    service = IngredientService(db)

    return service.get_all()


@router.get(
    "/{ingredient_id}",
    response_model=IngredientResponse,
    status_code=status.HTTP_200_OK,
)
def get_ingredient_by_id(
    ingredient_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> IngredientResponse:
    service = IngredientService(db)

    try:
        return service.get_by_id(ingredient_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(
    data: IngredientCreate,
    db: Annotated[Session, Depends(get_db)],
) -> IngredientResponse:
    service = IngredientService(db)

    return service.create(data)


@router.put(
    "/{ingredient_id}",
    response_model=IngredientResponse,
    status_code=status.HTTP_200_OK,
)
def update_ingredient(
    ingredient_id: Annotated[int, Path(gt=0)],
    data: IngredientUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> IngredientResponse:
    service = IngredientService(db)

    try:
        return service.update(
            ingredient_id=ingredient_id,
            data=data,
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ingredient(
    ingredient_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = IngredientService(db)

    try:
        service.delete(ingredient_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error