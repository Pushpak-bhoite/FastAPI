from fastapi import APIRouter

from app.api.routers import users, posts, assets, users_list
from app.core.config import settings

api_router = APIRouter()

# Users list route (for AG Grid)
api_router.include_router(users_list.router)

# User management routes (registration, login, etc.)
api_router.include_router(users.router)

# Asset management routes
api_router.include_router(assets.router)

# api_router.include_router(posts.router) # commenting temporarly
# api_router.include_router(login.router)
# api_router.include_router(utils.router)
# api_router.include_router(items.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
