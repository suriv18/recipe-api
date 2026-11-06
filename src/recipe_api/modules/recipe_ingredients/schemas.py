from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RecipeIngredientCreate(BaseModel):
    item_number: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    ingredient_id: int = Field(
        ...,
        gt=0,
        examples=[5],
    )

    quantity_text: str | None = Field(
        default=None,
        max_length=30,
        examples=["500"],
    )

    quantity: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=3,
        examples=[Decimal("500.000")],
    )

    unit_id: int | None = Field(
        default=None,
        gt=0,
        examples=[2],
    )

    preparation: str | None = Field(
        default=None,
        max_length=300,
        examples=["cortado en cubos"],
    )

    original_text: str = Field(
        ...,
        min_length=1,
        max_length=400,
        examples=["500 g de pescado cortado en cubos"],
    )


class RecipeIngredientUpdate(BaseModel):
    item_number: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    ingredient_id: int = Field(
        ...,
        gt=0,
        examples=[5],
    )

    quantity_text: str | None = Field(
        default=None,
        max_length=30,
        examples=["250"],
    )

    quantity: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=3,
        examples=[Decimal("250.000")],
    )

    unit_id: int | None = Field(
        default=None,
        gt=0,
        examples=[2],
    )

    preparation: str | None = Field(
        default=None,
        max_length=300,
        examples=["cortado en cubos pequeños"],
    )

    original_text: str = Field(
        ...,
        min_length=1,
        max_length=400,
        examples=["250 g de pescado cortado en cubos pequeños"],
    )


class RecipeIngredientResponse(BaseModel):
    id: int
    recipe_id: int
    item_number: int
    ingredient_id: int
    quantity_text: str | None
    quantity: Decimal | None
    unit_id: int | None
    preparation: str | None
    original_text: str

    model_config = ConfigDict(
        from_attributes=True
    )