import fastapi


def http403_exc_forbidden() -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail="Unable to validate credentials!",
    )
