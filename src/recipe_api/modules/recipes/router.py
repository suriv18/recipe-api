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
from recipe_api.modules.recipes.schemas import (
    RecipeCreate,
    RecipeResponse,
    RecipeUpdate,
)
from recipe_api.modules.recipes.service import RecipeService


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)


@router.get(
    "",
    response_model=list[RecipeResponse],
    status_code=status.HTTP_200_OK,
)
def get_recipes(
    db: Annotated[Session, Depends(get_db)],
) -> list[RecipeResponse]:
    service = RecipeService(db)

    return service.get_all()


@router.get(
    "/{recipe_id}",
    response_model=RecipeResponse,
    status_code=status.HTTP_200_OK,
)
def get_recipe_by_id(
    recipe_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> RecipeResponse:
    service = RecipeService(db)

    try:
        return service.get_by_id(recipe_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_recipe(
    data: RecipeCreate,
    db: Annotated[Session, Depends(get_db)],
) -> RecipeResponse:
    service = RecipeService(db)

    try:
        return service.create(data)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.put(
    "/{recipe_id}",
    response_model=RecipeResponse,
    status_code=status.HTTP_200_OK,
)
def update_recipe(
    recipe_id: Annotated[int, Path(gt=0)],
    data: RecipeUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> RecipeResponse:
    service = RecipeService(db)

    try:
        return service.update(
            recipe_id=recipe_id,
            data=data,
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_recipe(
    recipe_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = RecipeService(db)

    try:
        service.delete(recipe_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error