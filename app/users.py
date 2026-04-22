import uuid 
from typing import Optional
from annotated_types import T
from fastapi import Depends, Request
import fastapi
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
import fastapi_users
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport, 
    JWTStrategy
)

from fastapi_users.db import SQLAlchemyUserDatabase
from app.core.db import User, get_user_db
from app.core.permit_service import sync_user_to_permit

SECRET ="PushpakSecret"

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    User Manager for fastapi-users.
    
    Handles user lifecycle events like registration, password reset, etc.
    Now includes Permit.io integration to sync users for authorization.
    """
    reset_password_token_secret = SECRET
    verification_token_secret  = SECRET
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Called after a new user successfully registers.
        
        This is the hook where we sync the user to Permit.io.
        At registration time, user may not have an organization yet.
        They will be synced again when assigned to an organization.
        
        Args:
            user: The newly registered user
            request: The FastAPI request (optional)
        """
        print(f"User {user.id} has registered")
        
        # Sync user to Permit.io for authorization
        # Note: organization_id may be None at registration
        # User will be re-synced when assigned to an organization
        await sync_user_to_permit(
            user_id=str(user.id),
            email=user.email,
            organization_id=str(user.organization_id) if user.organization_id else None,
            organization_type=None  # Will be set when assigned to org
        )
        
    async def on_after_forgot_password(self, user: User, token:str, request:Optional[Request] = None):
        """Called when user requests password reset."""
        print(f"User {user.id} has forgot their password. Reset token ")
        
    async def on_after_request_verify(self, user:User, token:str, request: Optional[Request]= None):
        """Called when user requests email verification."""
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        
# we have defined this function to manage user 
async def get_user_manager(user_db: SQLAlchemyUserDatabase =Depends(get_user_db)):
    yield UserManager(user_db)

# endpnt to hit for login
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=36 * 10000 )

auth_backend = AuthenticationBackend(
    name="jwt", 
    transport=bearer_transport, 
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
# get current active user 
current_active_user = fastapi_users.current_user(active=True)