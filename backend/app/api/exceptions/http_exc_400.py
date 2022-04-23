import fastapi

from app.resources.http_exc_details import http_400_details


async def http400_exc_credentials_bad_request() -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_details(),
    )


async def http400_exc_bad_username_request(username: str) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_details(username=username),
    )


async def http400_exc_bad_email_request(email: str) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_details(email=email),
    )
