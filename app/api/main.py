from fastapi import APIRouter

from app.api.routers import users, posts, assets
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(posts.router)
api_router.include_router(assets.router)
# api_router.include_router(login.router)
# api_router.include_router(utils.router)
# api_router.include_router(items.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
