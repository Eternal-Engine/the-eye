# type: ignore
import datetime

import pydantic

from app.models.domain import base as base_model


def test_convert_datetime_into_str_datatype():

    string_datetime = base_model.convert_datetime_into_string(date_time=datetime.datetime.utcnow())

    assert string_datetime[-1] == "Z"
    assert isinstance(string_datetime, str)


def test_convert_field_into_camel_case():

    field = "created_at"
    camel_case_created_at_field = base_model.convert_field_to_camel_case(string=field)

    assert camel_case_created_at_field == "CreatedAt"


def test_iW_base_model_construction():

    model = base_model.IWBaseModel
    pydantic_base_model = pydantic.BaseModel
    pydantic_base_config = pydantic.BaseConfig

    expected_json_encoders = {datetime.datetime: base_model.convert_datetime_into_string}

    assert issubclass(model, pydantic_base_model)
    assert issubclass(model.Config, pydantic_base_config)
    assert model.Config.allow_population_by_field_name is True
    assert model.Config.json_encoders == expected_json_encoders
    assert model.Config.alias_generator == base_model.convert_field_to_camel_case
