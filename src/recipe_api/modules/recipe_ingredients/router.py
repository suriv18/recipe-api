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
from recipe_api.modules.recipe_ingredients.schemas import (
    RecipeIngredientCreate,
    RecipeIngredientResponse,
    RecipeIngredientUpdate,
)
from recipe_api.modules.recipe_ingredients.service import (
    RecipeIngredientService,
)


router = APIRouter(
    prefix="/recipes/{recipe_id}/ingredients",
    tags=["Recipe Ingredients"],
)


@router.get(
    "",
    response_model=list[RecipeIngredientResponse],
    status_code=status.HTTP_200_OK,
)
def get_recipe_ingredients(
    recipe_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> list[RecipeIngredientResponse]:
    service = RecipeIngredientService(db)

    try:
        return service.get_all_by_recipe(recipe_id)

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/{recipe_ingredient_id}",
    response_model=RecipeIngredientResponse,
    status_code=status.HTTP_200_OK,
)
def get_recipe_ingredient_by_id(
    recipe_id: Annotated[int, Path(gt=0)],
    recipe_ingredient_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> RecipeIngredientResponse:
    service = RecipeIngredientService(db)

    try:
        return service.get_by_id(
            recipe_id=recipe_id,
            recipe_ingredient_id=recipe_ingredient_id,
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=RecipeIngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_recipe_ingredient(
    recipe_id: Annotated[int, Path(gt=0)],
    data: RecipeIngredientCreate,
    db: Annotated[Session, Depends(get_db)],
) -> RecipeIngredientResponse:
    service = RecipeIngredientService(db)

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
    "/{recipe_ingredient_id}",
    response_model=RecipeIngredientResponse,
    status_code=status.HTTP_200_OK,
)
def update_recipe_ingredient(
    recipe_id: Annotated[int, Path(gt=0)],
    recipe_ingredient_id: Annotated[int, Path(gt=0)],
    data: RecipeIngredientUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> RecipeIngredientResponse:
    service = RecipeIngredientService(db)

    try:
        return service.update(
            recipe_id=recipe_id,
            recipe_ingredient_id=recipe_ingredient_id,
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
    "/{recipe_ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_recipe_ingredient(
    recipe_id: Annotated[int, Path(gt=0)],
    recipe_ingredient_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    service = RecipeIngredientService(db)

    try:
        service.delete(
            recipe_id=recipe_id,
            recipe_ingredient_id=recipe_ingredient_id,
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error