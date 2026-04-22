from fastapi import APIRouter

from app.api.routers import users, posts, assets, organizations
from app.core.config import settings

api_router = APIRouter()

# User management routes (registration, login, etc.)
api_router.include_router(users.router)

# Organization management routes (CRUD with Permit.io authorization)
api_router.include_router(organizations.router)

# Asset management routes
api_router.include_router(assets.router)

# api_router.include_router(posts.router) # commenting temporarly
# api_router.include_router(login.router)
# api_router.include_router(utils.router)
# api_router.include_router(items.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
