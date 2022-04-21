from typing import Optional

import pydantic

from app.models.domain.users import User
from app.models.schemas.base import IWBaseSchema  # type: ignore


class UserInLogin(IWBaseSchema):  # type: ignore
    email: pydantic.EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str
    is_publisher: bool = False


class UserInUpdate(pydantic.BaseModel):
    username: Optional[str] = None
    email: Optional[pydantic.EmailStr] = None
    password: Optional[str] = None
    is_publisher: Optional[bool] = False


class UserWithToken(User):  # type: ignore
    token: str


class UserInResponse(IWBaseSchema):  # type: ignore
    user: UserWithToken
