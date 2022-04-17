import pydantic


class IDModelMixin(pydantic.BaseModel):
    id_: int = pydantic.Field(1, alias="id")
