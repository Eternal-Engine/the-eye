import fastapi
from fastapi import security as fastapi_security
from starlette import exceptions as starlette_exc, requests as starlette_req


class IWAPIKeyHeader(fastapi_security.APIKeyHeader):
    async def __call__(self, request: starlette_req.Request):
        try:
            return await super().__call__(request)
        except starlette_exc.HTTPException as auth_exc:
            raise fastapi.HTTPException(
                status_code=auth_exc.status_code,
                detail="Authentication required!",
            )
