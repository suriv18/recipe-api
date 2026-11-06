from pydantic import BaseModel, ConfigDict, Field


class UnitCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=20,
        examples=["kg"],
    )


class UnitUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=20,
        examples=["gramos"],
    )


class UnitResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )