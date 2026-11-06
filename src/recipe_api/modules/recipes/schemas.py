from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Ceviche"],
    )

    area_id: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    category_id: int = Field(
        ...,
        gt=0,
        examples=[2],
    )


class RecipeUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Ceviche clásico"],
    )

    area_id: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    category_id: int = Field(
        ...,
        gt=0,
        examples=[2],
    )


class RecipeResponse(BaseModel):
    id: int
    name: str
    area_id: int
    category_id: int

    model_config = ConfigDict(
        from_attributes=True
    )