# type: ignore
import datetime

from app.models.base_models import convert_datetime_into_string


def test_convert_datetime_into_str_datatype():

    string_datetime = convert_datetime_into_string(date_time=datetime.datetime.utcnow())

    assert string_datetime[-1] == "Z"
    assert isinstance(string_datetime, str)
