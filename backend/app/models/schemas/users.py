from typing import Optional

import pydantic

from app.models.domain import users as users_domain
from app.models.schemas import base as base_schema


class UserInLogin(base_schema.IWBaseSchema):  # type: ignore
    email: pydantic.EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(pydantic.BaseModel):
    username: Optional[str] = None
    email: Optional[pydantic.EmailStr] = None
    password: Optional[str] = None


class UserWithToken(users_domain.User):  # type: ignore
    token: str


class UserInResponse(base_schema.IWBaseSchema):  # type: ignore
    user: UserWithToken
