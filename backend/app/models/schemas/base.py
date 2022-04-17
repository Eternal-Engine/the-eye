# type: ignore
from app.models.domain import base as base_domain


class IWBaseSchema(base_domain.IWBaseModel):
    class Config(base_domain.IWBaseModel.Config):
        orm_mode = True
