# type: ignore
# fmot: off
import datetime


def convert_datetime_into_string(date_time: datetime.datetime) -> str:
    return date_time.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:

    return "".join(word.capitalize() or "_" for word in string.split("_"))


class IWBaseModel:
    pass
