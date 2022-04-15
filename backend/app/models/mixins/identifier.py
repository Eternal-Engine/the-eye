import pydantic


class IDModelMixin(pydantic.BaseModel):
    id_: int = pydantic.Field(0, alias="id")
