# type: ignore
# fmot: off
import datetime


def convert_datetime_into_string(date_time: datetime.datetime) -> str:
    return date_time.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")
