import datetime

import pydantic

from app.models.mixin_models.datetime_mixin_models import DateTimeModelMixin


def test_datetime_model_mixin_construction():

    datetime_mixin = DateTimeModelMixin(created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
    pydantic_base_model = pydantic.BaseModel

    assert issubclass(type(datetime_mixin), pydantic_base_model)
    assert isinstance(datetime_mixin.created_at, datetime.datetime)
    assert isinstance(datetime_mixin.updated_at, datetime.datetime)
