import fastapi


async def http400_exc_credentials_bad_request() -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail="Login failed! Re-check heck your email and password!",
    )


async def http400_exc_bad_username_request(username: str) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=f"The username {username} is taken! Be creative and choose another one!",
    )


async def http400_exc_bad_email_request(email: str) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=f"The email {email} is taken! Be creative and choose another one!",
    )
