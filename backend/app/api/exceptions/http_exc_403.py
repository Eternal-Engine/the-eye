import fastapi

from app.resources.http_exc_details import HTTP_300_DETAILS


async def http403_exc_forbidden() -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail=HTTP_300_DETAILS,
    )
