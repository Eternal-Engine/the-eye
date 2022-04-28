import fastapi
from app.db.repositories.tags import TagsRepository
from app.api.dependencies.database import get_repository
from app.models.schemas.tags import Tag, TagInResponse


router=fastapi.APIRouter(
    prefix="/tags"
)

@router.post("/", response_model=TagInResponse)
async def create_hash_tag(word: str, tags_repo: TagsRepository=fastapi.Depends(get_repository(TagsRepository))):
    new_hashtag = await tags_repo.create(word=word)
    return TagInResponse(
        tag=Tag(
            hashtag=new_hashtag.hashtag
        
        )
    ) 