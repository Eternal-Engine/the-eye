from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin
from app.models.schemas.base import IWBaseSchema


class Tag(IWBaseSchema):
    hashtag: str = ""


class TagInDB(Tag, IDModelMixin, DateTimeModelMixin):
    prefix: str = "#"

    def generate_hash_tag(self, word):
        self.hashtag = self.prefix + word


class TagInResponse(Tag):
    tag: Tag
