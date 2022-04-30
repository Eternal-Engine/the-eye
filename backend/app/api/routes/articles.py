from typing import List

import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.repository import get_repository
from app.db.repositories.articles import ArticlesRepository
from app.models.domain.articles import ArticleInDB
from app.models.domain.users import User
from app.models.schemas.articles import ArticleInCreate, ArticleInResponse

router = fastapi.APIRouter(prefix="/articles", tags=["articles"])


@router.post(
    path="",
    response_model=ArticleInResponse,
    name="journalists:create-article-for-user-profile",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_article_for_user_profile(
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    article_create: ArticleInCreate = fastapi.Body(..., embed=True, alias="article"),
    articles_repo: ArticlesRepository = fastapi.Depends(get_repository(ArticlesRepository)),
) -> ArticleInResponse:  # type: ignore

    new_article = await articles_repo.create_articles(journalist_id=current_user.id_, **article_create.dict())

    return ArticleInResponse(
        article=ArticleInDB(
            headline=new_article.headline,
            description=new_article.description,
            slug=new_article.slug,
            body=new_article.body,
            is_drafted=new_article.is_drafted,
            author_id=new_article.author_id,
        )
    )


@router.get(path="", name="journalists:retrieve-all-journalists", response_model=List[ArticleInResponse])
async def retrieve_all_articles(
    articles_repo: ArticlesRepository = fastapi.Depends(get_repository(ArticlesRepository)),
) -> List[ArticleInResponse]:

    db_articles = await articles_repo.get_articles()
    db_articles_list = []

    for article in db_articles:
        article = ArticleInResponse(
            article=ArticleInDB(
                headline=article.headline,
                description=article.description,
                slug=article.slug,
                body=article.body,
                is_drafted=article.is_drafted,
                author_id=article.author_id,
            )
        )
        db_articles_list.append(article)

    return db_articles_list
