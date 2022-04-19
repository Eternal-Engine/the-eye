# type: ignore
from app.models.domain.base import IWBaseModel


class IWBaseSchema(IWBaseModel):
    class Config(IWBaseModel.Config):
        orm_mode = True
