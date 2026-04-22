"""
FastAPI Dependencies for Authorization

This module provides reusable dependencies for route protection using Permit.io.
Use these dependencies to enforce permissions on your API endpoints.

Dependencies:
- get_user_organization: Loads the user's organization from DB
- require_permission: Factory that creates permission checker for resource/action
- require_organization_permission: Specialized checker for organization hierarchy
- PermissionChecker: Class-based checker for complex scenarios

Usage Example:
    @router.get("/assets")
    async def list_assets(
        user: User = Depends(current_active_user),
        _: None = Depends(require_permission("asset", "read"))
    ):
        # This code only runs if user has permission to read assets
        ...
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import User, Organization, get_db
from app.users import current_active_user
from app.core.permit_service import check_permission, check_organization_permission


# =============================================================================
# ORGANIZATION DEPENDENCY
# =============================================================================

async def get_user_organization(
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Optional[Organization]:
    """
    Get the organization for the current user.
    
    This dependency loads the user's organization from the database.
    Use this when you need organization context for permission checks.
    
    Returns:
        Organization object or None if user has no organization
        
    Usage:
        @router.get("/my-org")
        async def get_my_org(
            org: Organization = Depends(get_user_organization)
        ):
            return org
    """
    # If user doesn't belong to any organization, return None
    if not user.organization_id:
        return None
    
    # Query the organization from database
    result = await db.execute(
        select(Organization).where(Organization.id == user.organization_id)
    )
    return result.scalars().first()


# =============================================================================
# PERMISSION DEPENDENCY FACTORIES
# =============================================================================

def require_permission(resource: str, action: str):
    """
    Dependency factory that creates a permission checker for a specific resource/action.
    
    This is a higher-order function that returns a dependency.
    The returned dependency will raise 403 Forbidden if the user lacks permission.
    
    Args:
        resource: The resource type (organization, asset, monitor)
        action: The action (create, read, update, delete)
        
    Returns:
        A FastAPI dependency function
        
    Usage:
        # Single permission check
        @router.post("/assets")
        async def create_asset(
            user: User = Depends(current_active_user),
            _: None = Depends(require_permission("asset", "create"))
        ):
            # This code only runs if user has permission
            ...
            
        # Multiple permissions (all must pass)
        @router.post("/assets/{id}/monitors")
        async def create_monitor(
            _asset: None = Depends(require_permission("asset", "read")),
            _monitor: None = Depends(require_permission("monitor", "create"))
        ):
            ...
    """
    async def permission_dependency(
        user: User = Depends(current_active_user),
        organization: Optional[Organization] = Depends(get_user_organization)
    ):
        # Get tenant ID (organization ID) for the permission check
        # This scopes the permission check to the user's organization context
        tenant_id = str(organization.id) if organization else None
        
        # Check permission with Permit.io
        permitted = await check_permission(
            user_id=str(user.id),
            action=action,
            resource=resource,
            tenant_id=tenant_id
        )
        
        # Raise 403 if not permitted
        if not permitted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You don't have permission to {action} {resource}"
            )
        
        # Return None - dependency is just for validation
        return None
    
    return permission_dependency


def require_organization_permission(action: str):
    """
    Dependency for organization-specific permission checks.
    
    This handles the hierarchical permission logic for organizations:
    - assetwatch can access all organizations
    - reseller can access self and their reseller_customers
    - customer/reseller_customer can only access self
    
    Args:
        action: The action (create, read, update, delete)
        
    Returns:
        A FastAPI dependency function
        
    Usage:
        @router.get("/organizations/{org_id}")
        async def get_organization(
            org_id: str,
            _: None = Depends(require_organization_permission("read"))
        ):
            ...
    """
    async def permission_dependency(
        target_org_id: str,  # This comes from path parameter
        user: User = Depends(current_active_user),
        organization: Optional[Organization] = Depends(get_user_organization)
    ):
        # User must belong to an organization
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User must belong to an organization"
            )
        
        # Check permission using our custom hierarchy logic
        permitted = await check_organization_permission(
            user_id=str(user.id),
            action=action,
            target_organization_id=target_org_id,
            user_organization_id=str(organization.id),
            user_organization_type=organization.organization_type
        )
        
        if not permitted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You don't have permission to {action} this organization"
            )
        
        return None
    
    return permission_dependency


# =============================================================================
# PERMISSION CHECKER CLASS
# =============================================================================

class PermissionChecker:
    """
    Class-based permission checker for more complex scenarios.
    
    Use this when you need to:
    - Check permissions with dynamic resource attributes
    - Check multiple permissions in sequence
    - Make decisions based on organization type
    
    Usage:
        @router.post("/organizations")
        async def create_organization(
            user: User = Depends(current_active_user),
            organization: Organization = Depends(get_user_organization)
        ):
            checker = PermissionChecker(user, organization)
            
            # Check if user can create organizations
            if not await checker.can("create", "organization"):
                raise HTTPException(403, "Permission denied")
            
            # Additional checks based on org type
            if checker.is_reseller():
                # Resellers can only create reseller_customer
                ...
    """
    
    def __init__(self, user: User, organization: Optional[Organization]):
        """
        Initialize the permission checker.
        
        Args:
            user: The current authenticated user
            organization: The user's organization (can be None)
        """
        self.user = user
        self.organization = organization
        self.user_id = str(user.id)
        self.tenant_id = str(organization.id) if organization else None
        self.org_type = organization.organization_type if organization else None
    
    async def can(
        self, 
        action: str, 
        resource: str,
        resource_attributes: Optional[dict] = None
    ) -> bool:
        """
        Check if the user can perform an action on a resource.
        
        Args:
            action: The action (create, read, update, delete)
            resource: The resource type
            resource_attributes: Additional attributes for ABAC
            
        Returns:
            True if permitted, False otherwise
        """
        return await check_permission(
            user_id=self.user_id,
            action=action,
            resource=resource,
            tenant_id=self.tenant_id,
            resource_attributes=resource_attributes
        )
    
    async def can_manage_organization(
        self, 
        target_org_id: str, 
        action: str
    ) -> bool:
        """
        Check if user can manage a specific organization.
        
        This handles the hierarchical permission logic for organizations.
        
        Args:
            target_org_id: ID of the organization to manage
            action: The action to perform
            
        Returns:
            True if permitted, False otherwise
        """
        if not self.organization:
            return False
            
        return await check_organization_permission(
            user_id=self.user_id,
            action=action,
            target_organization_id=target_org_id,
            user_organization_id=str(self.organization.id),
            user_organization_type=self.org_type
        )
    
    # =============================================================================
    # ORGANIZATION TYPE HELPERS
    # These methods make it easy to check the user's organization type
    # =============================================================================
    
    def is_assetwatch(self) -> bool:
        return self.org_type == "assetwatch"
    
    def is_reseller(self) -> bool:
        return self.org_type == "reseller"
    
    def is_customer(self) -> bool:
        return self.org_type == "customer"
    
    def is_reseller_customer(self) -> bool:
        return self.org_type == "reseller_customer"
    
    def has_organization(self) -> bool:
        return self.organization is not None
