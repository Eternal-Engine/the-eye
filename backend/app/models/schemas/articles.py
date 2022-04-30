from typing import List, Optional

import pydantic

from app.models.domain.articles import Article, ArticleInDB
from app.models.schemas.base import IWBaseSchema  # type: ignore
from app.models.schemas.tags import Tag


class ArticleInCreate(IWBaseSchema):
    headline: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    # images: Optional [List[Image]] = None
    # videos: Optional [List[Video] = None
    # audios: Optional [List[Audio]] = None
    # tags: Optional[List[Tag]] = None
    is_drafted: Optional[bool] = None


class ArticleInUpdate(pydantic.BaseModel):
    headline: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    # images: Optional [List[Image]] = None
    # videos: Optional [List[Video] = None
    # audios: Optional [List[Audio]] = None
    # tags: Optional[List[Tag]] = None
    is_drafted: Optional[bool] = None


class ArticleWithTags(Article):
    tags: List[Tag]


class ArticleInResponse(IWBaseSchema):
    article: ArticleInDB
