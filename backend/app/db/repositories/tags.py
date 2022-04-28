# type: ignore
from sys import prefix
from typing import Any, List, Optional

from pyparsing import WordStart

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.schemas.tags import Tag, TagInDB


Class TagsRepository(BaseRepository)
    async def create(self, *, word):
        db_tag = TagInDB()
        db_tag.generate_hash_tag(word=word)
        async with self.connection.transaction():
            new_tag = await queries.create_new_tag(
                self.connection,
                prefix=db_tag.prefix,
                hashtag=db_tag.hashtag
            )
        return db_tag.copy(update=dict(new_tag))


    async def read(self) -> List[Tag]:
        async with self.connection.transaction():
            db_tags = await queries.read_tags(self.connection)
            db_tags_list = []

            for db_tag in db_tags:

                db_tags_list.append(Tag(**db_tag))

        return db_tags_list 