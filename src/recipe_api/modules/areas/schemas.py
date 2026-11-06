from pydantic import BaseModel, ConfigDict, Field


class AreaCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["Peruana"],
    )


class AreaUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["Italiana"],
    )


class AreaResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )