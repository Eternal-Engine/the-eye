import fastapi

router = fastapi.APIRouter(prefix="/authentication", tags=["Authentication"])


@router.post(
    path="/signup",
)
async def registration():
    pass


@router.post(
    path="/signin",
)
async def signin():
    pass
