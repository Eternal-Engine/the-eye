import datetime

import pydantic


class JWToken(pydantic.BaseModel):

    expiration_date: datetime.datetime
    subject: str


class JWTUser(pydantic.BaseModel):
    username: str
