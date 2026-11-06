from pydantic import BaseModel, ConfigDict, Field


class IngredientCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Tomate"],
    )


class IngredientUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Tomate cherry"],
    )


class IngredientResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )