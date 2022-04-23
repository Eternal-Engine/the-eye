import fastapi

from app.resources.http_exc_details import http_404_details


async def http404_exc_id_not_found(id: int) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_details(id=id),
    )


async def http404_exc_username_not_found(username: str) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_details(username=username),
    )
