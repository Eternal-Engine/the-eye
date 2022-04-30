import slugify

from app.models.domain.base import IWBaseModel
from app.models.domain.journalists import Journalist
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin


class Article(IWBaseModel):

    headline: str
    description: str
    body: str
    # images: List[Image]
    # videos: List[Video]
    # audios: List[Audio]
    # tags: List[Tag]
    # comments: List[Comment]
    # likes: List[Like]
    author: Journalist
    author_id: int
    is_drafted: bool = False


class ArticleInDB(Article, IDModelMixin, DateTimeModelMixin):
    slug = ""

    def generate_slug(self, headline, journalist_id, article_id):
        self.slug = slugify.slugify(f"{headline}-{journalist_id}{article_id}")
