from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.crud import users as user_crud
from app.models.schemas import users as user_schemas

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/create/", response_model=user_schemas.UserInResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: user_schemas.UserInCreate):
    new_user_id = await user_crud.create_user(payload)

    db_user = {
        "id": new_user_id,
        "username": payload.username,
        "email": payload.email,
        "is_publisher": payload.is_publisher,
        "is_premium_account": payload.is_premium_account,
        "is_verified": payload.is_verified,
        "is_active": payload.is_active,
    }

    return db_user


@router.get("/", response_model=List[user_schemas.UserInResponse], status_code=status.HTTP_200_OK)
async def retrieve_all_users():

    return await user_crud.get_all_users()


@router.get("/id/{user_id}", response_model=user_schemas.UserInResponse, status_code=status.HTTP_200_OK)
async def retrieve_user_by_id(user_id: int):

    db_user = await user_crud.get_user_by_id(user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.put("/id/{user_id}/", response_model=user_schemas.UserInResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, payload: user_schemas.UserInUpdate):
    db_user = await user_crud.get_user_by_id(user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    user_id = await user_crud.update_user(user_id, payload)

    updated_db_user = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "is_publisher": payload.is_publisher,
        "is_premium_account": payload.is_premium_account,
        "is_verified": payload.is_verified,
        "is_active": payload.is_active,
    }

    return updated_db_user


@router.delete("/id/{user_id}/", response_model=user_schemas.UserInResponse, status_code=status.HTTP_202_ACCEPTED)
async def remove_user(user_id: int):
    db_user = await user_crud.get_user_by_id(user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    await user_crud.delete_user(user_id)

    return db_user
