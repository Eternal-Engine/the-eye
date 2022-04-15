import datetime

import pydantic


class DateTimeModelMixin(pydantic.BaseModel):
    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

    @pydantic.validator("created_at", "updated_at", pre=True)
    def default_datetime(
        cls,  # noqa: N805
        value: datetime.datetime,  # noqa: WPS110
    ) -> datetime.datetime:
        return value or datetime.datetime.now()
