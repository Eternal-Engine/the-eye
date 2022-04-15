import pydantic

from app.models.mixin_models.id_mixin_models import IDModelMixin


def test_datetime_model_mixin_construction():

    id_mixin = IDModelMixin(id=1)
    pydantic_base_model = pydantic.BaseModel

    assert issubclass(type(id_mixin), pydantic_base_model)
    assert isinstance(id_mixin.id_, int)
    assert id_mixin.id_ == 1
