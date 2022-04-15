# type: ignore
import datetime

from app.models.base_models import convert_datetime_into_string, convert_field_to_camel_case


def test_convert_datetime_into_str_datatype():

    string_datetime = convert_datetime_into_string(date_time=datetime.datetime.utcnow())

    assert string_datetime[-1] == "Z"
    assert isinstance(string_datetime, str)


def test_convert_field_into_camel_case():

    field = "created_at"
    camel_case_created_at_field = convert_field_to_camel_case(string=field)

    assert camel_case_created_at_field == "CreatedAt"
