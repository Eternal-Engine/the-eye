import fastapi


async def http404_exc_id_not_found(id: int) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=f"Either the user with ID {id} is deleted, or you are not authorized; Check your authorization!",
    )


async def http404_exc_username_not_found(username: str) -> Exception:
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=f"Either the user {username} is deleted, or you are not authorized; Check your authorization!",
    )
