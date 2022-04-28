from re import I
from asyncpg import connection as asyncpg_conn
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.db.repositories.journalists import JournalistsRepository
from typing import Optional, List, Any
from app.models.domain.articles import Article, ArticleInDB
from app.models.domain.journalists import Journalist


class ArticlesRepository(BaseRepository):
    def __init__(self, conn: asyncpg_conn.Connection):
        super().__init__(conn)
        self._journalists_repo = JournalistsRepository(conn)

    async def create_articles(
        self,
        *,
        journalist_id: int,
        headline: str = "",
        description: str = "",
        body: str = "",
        author: Journalist,
        #images: Optional [List[Image]] = None,
        # videos: Optional [List[Video] = None,
        #audios: Optional [List[Audio]] = None,
        #tags: Optional[Tag] = None,
        is_drafted: bool = False

    ) -> ArticleInDB:

        db_journalist = await self._journalists_repo.get_journalist_by_user_id(id=journalist_id)
        db_article = ArticleInDB(
            headline=headline, description=description, body=body, author_id=db_journalist.id_, is_drafted=is_drafted
        )
        print(db_article.id_)
        db_article.generate_slug(
            headline=headline, journalist_id=journalist_id, article_id=db_article.id_)
        async with self.connection.transaction():

            new_article = await queries.create_new_article(
                self.connection,
                headline=db_article.headline,
                slug=db_article.slug,
                description=db_article.description,
                body=db_article.body,
                is_drafted=db_article.is_drafted,
                author_id=db_journalist.id_
            )
        return db_article.copy(update=dict(new_article))

    async def get_articles(self) -> List[ArticleInDB]:
        async with self.connection.transaction():
            db_articles = await queries.read_articles(self.connection)
            db_articles_list = []

            for db_article in db_articles:

                db_articles_list.append(ArticleInDB(**db_article))

            return db_articles_list

    async def get_article_by_id(self, *, id: int) -> ArticleInDB:

        db_article = await queries.read_article_by_id(self.connection, id=id)

        if db_article:

            return ArticleInDB(**db_article)

        raise EntityDoesNotExist(f"Article with id {id} does not exist!")

    async def update_article(
        self,
        *,
        article: Article,
        headline: Optional[str] = None,
        description: Optional[str] = None,
        body: Optional[str] = None,
        #images: Optional [List[Image]] = None
        # videos: Optional [List[Video] = None
        #audios: Optional [List[Audio]] = None
        #tags: Optional[List[Tag]] = None,
    ) -> ArticleInDB:

        db_article = await self.get_article_by_id(id=article.id_)

        if db_article:
            db_article.headline = headline or db_article.headline
            db_article.description = description or db_article.description
            db_article.body = body or db_article.body

            async with self.connection.transaction():
                db_article.updated_at = await queries.update_article_by_id(
                    self.connection,
                    id=article.id_,
                    new_headline=db_article.headline,
                    new_description=db_article.description,
                    new_body=db_article.body
                )

            return db_article

        raise EntityDoesNotExist("Article with that Headline does not exist!")

    async def delete_article(self, *, id: int) -> Any:

        try:
            return await queries.delete_article_by_id(self.connection, id=id)

        except EntityDoesNotExist as value_error:

            raise ValueError(
                f"Article with id {id} does not exist!") from value_error
