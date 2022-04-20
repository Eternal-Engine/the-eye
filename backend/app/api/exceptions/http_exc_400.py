import fastapi


def http400_exc_bad_request() -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail="Incorrect login credentials, check your email or password!",
    )
