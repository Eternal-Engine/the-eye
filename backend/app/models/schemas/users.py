from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserAsBase(BaseModel):
    username: str
    email: EmailStr
    is_publisher: bool = False
    is_premium_account: bool = False
    is_verified: bool = False
    is_active: bool = True


class UserInCreate(UserAsBase):
    password: str


class UserInLogin(BaseModel):
    email: EmailStr
    password: str
    last_logged_in_at: datetime


class UserInUpdate(UserAsBase):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    updated_at: Optional[datetime]
    username_updated_at: Optional[datetime]
    email_updated_at: Optional[datetime]
    password_updated_at: Optional[datetime]
    is_publisher: Optional[bool]
    is_premium_account: Optional[bool]
    is_verified: Optional[bool]
    is_active: Optional[bool]


class UserInResponse(UserAsBase):
    id: int
    created_at: datetime | None
    updated_at: datetime | None
    last_logged_in_at: datetime | None
    username_updated_at: datetime | None
    email_updated_at: datetime | None
    password_updated_at: datetime | None
    is_publisher: bool
    is_premium_account: bool
    is_verified: bool
    is_active: bool

    class Config:
        orm_mode = True
