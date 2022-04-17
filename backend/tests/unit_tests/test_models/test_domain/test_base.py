# type: ignore
import datetime

import pydantic

from app.models.domain import base as base_domain


def test_convert_datetime_into_str_datatype():

    string_datetime = base_domain.convert_datetime_into_string(date_time=datetime.datetime.utcnow())

    assert string_datetime[-1] == "Z"
    assert isinstance(string_datetime, str)


def test_convert_field_into_camel_case():

    field = "created_at"
    camel_case_created_at_field = base_domain.convert_field_to_camel_case(string=field)

    assert camel_case_created_at_field == "createdAt"


def test_iW_base_model_construction():

    domain_base_model = base_domain.IWBaseModel
    pydantic_base_model = pydantic.BaseModel
    pydantic_base_config = pydantic.BaseConfig

    expected_json_encoders = {datetime.datetime: base_domain.convert_datetime_into_string}

    assert issubclass(domain_base_model, pydantic_base_model)
    assert issubclass(domain_base_model.Config, pydantic_base_config)
    assert domain_base_model.Config.allow_population_by_field_name is True
    assert domain_base_model.Config.json_encoders == expected_json_encoders
    assert domain_base_model.Config.alias_generator == base_domain.convert_field_to_camel_case
