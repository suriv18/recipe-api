from pydantic import BaseModel, ConfigDict, Field


class StepCreate(BaseModel):
    step_number: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    description: str = Field(
        ...,
        min_length=1,
        examples=["Lavar y cortar los ingredientes."],
    )


class StepUpdate(BaseModel):
    step_number: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    description: str = Field(
        ...,
        min_length=1,
        examples=["Lavar, cortar y reservar los ingredientes."],
    )


class StepResponse(BaseModel):
    id: int
    recipe_id: int
    step_number: int
    description: str

    model_config = ConfigDict(
        from_attributes=True
    )