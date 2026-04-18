
from fastapi import APIRouter, Depends, HTTPException
from app.users import auth_backend, current_active_user, fastapi_users
from app.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate

router = APIRouter()

# connect diff auth endpoints that we need to our fast API users endpoints. 
router.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth - 1"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=["auth - 2"])
router.include_router(fastapi_users.get_reset_password_router(), prefix='/auth', tags=["auth - 3"])
router.include_router(fastapi_users.get_verify_router(UserRead), prefix='/auth', tags=["auth - 4 "])
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix='/users', tags=["users - 5"])
