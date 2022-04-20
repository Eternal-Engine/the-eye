from typing import Union

import fastapi
import pydantic
from fastapi.openapi.constants import REF_PREFIX as FASTAPI_REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition


async def http_error_handler(
    _: fastapi.requests.Request, exc: fastapi.HTTPException
) -> fastapi.responses.ORJSONResponse:
    return fastapi.responses.ORJSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def http422_error_handler(
    _: fastapi.requests.Request,
    exc: Union[fastapi.exceptions.RequestValidationError, pydantic.ValidationError],
) -> fastapi.responses.ORJSONResponse:
    return fastapi.responses.ORJSONResponse(
        {"errors": exc.errors()},
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": f"{FASTAPI_REF_PREFIX}ValidationError"},
    },
}
