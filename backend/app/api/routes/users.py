from fastapi import APIRouter, status

from app.api.crud import users as user_crud
from app.models.schemas import users as user_schemas

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/create/", response_model=user_schemas.UserInResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: user_schemas.UserInCreate):
    new_user = await user_crud.create_user(payload)

    response_object = {
        "id": new_user,
        "username": payload.username,
        "email": payload.email,
        "is_publisher": payload.is_publisher,
        "is_premium_account": payload.is_premium_account,
        "is_verified": payload.is_verified,
        "is_active": payload.is_active,
    }

    return response_object


@router.get("/id/{id}", response_model=user_schemas.UserInResponse)
async def read_note(id: int):
    db_user = await user_crud.get_user_by_id(id)

    return db_user
