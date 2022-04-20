import fastapi
from fastapi import security as fastapi_security


class IWAPIKeyHeader(fastapi_security.APIKeyHeader):
    async def __call__(self, request: fastapi.requests.Request):
        try:
            return await super().__call__(request)
        except fastapi.HTTPException as auth_exc:
            raise fastapi.HTTPException(
                status_code=auth_exc.status_code,
                detail="Authentication required!",
            ) from auth_exc
