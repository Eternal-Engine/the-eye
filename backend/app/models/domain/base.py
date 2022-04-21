import datetime

import pydantic


def convert_datetime_into_string(date_time: datetime.datetime) -> str:

    return date_time.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:

    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


class IWBaseModel(pydantic.BaseModel):
    """
    IWBaseModel: iWitness Base Model.
    The base class for all models in iWitness web application.
    """

    class Config(pydantic.BaseConfig):
        validate_assignment = True
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_into_string}
        alias_generator = convert_field_to_camel_case
