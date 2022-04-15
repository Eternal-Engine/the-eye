# type: ignore
from app.models.domain import base as base_model


class IWBaseSchema(base_model.IWBaseModel):
    class Config(base_model.IWBaseModel.Config):
        orm_mode = True
