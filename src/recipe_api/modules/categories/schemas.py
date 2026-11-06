from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["Postres"],
    )


class CategoryUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["Platos principales"],
    )


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )