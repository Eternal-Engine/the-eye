# type: ignore
import datetime

import pydantic

from app.models.domain.base import IWBaseModel, convert_datetime_into_string, convert_field_to_camel_case


def test_convert_datetime_into_str_datatype() -> None:

    string_datetime = convert_datetime_into_string(date_time=datetime.datetime.utcnow())

    assert string_datetime[-1] == "Z"
    assert isinstance(string_datetime, str)


def test_convert_field_into_camel_case() -> None:

    field = "created_at"
    camel_case_created_at_field = convert_field_to_camel_case(string=field)

    assert camel_case_created_at_field == "createdAt"


def test_iW_base_model_construction() -> None:

    domain_base_model = IWBaseModel
    pydantic_base_model = pydantic.BaseModel
    pydantic_base_config = pydantic.BaseConfig

    expected_json_encoders = {datetime.datetime: convert_datetime_into_string}

    assert issubclass(domain_base_model, pydantic_base_model)
    assert issubclass(domain_base_model.Config, pydantic_base_config)
    assert domain_base_model.Config.allow_population_by_field_name is True
    assert domain_base_model.Config.json_encoders == expected_json_encoders
    assert domain_base_model.Config.alias_generator == convert_field_to_camel_case
