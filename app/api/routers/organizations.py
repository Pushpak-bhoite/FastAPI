"""
Organization Management Router

This module handles CRUD operations for organizations with Permit.io authorization.
Organizations are the core of the multi-tenant RBAC system.

Permission Matrix:
┌─────────────────────┬────────┬────────┬────────┬────────┐
│ Role                │ Create │ Read   │ Update │ Delete │
├─────────────────────┼────────┼────────┼────────┼────────┤
│ assetwatch          │ ALL    │ ALL    │ ALL    │ ALL    │
│ reseller            │ OWN*   │ SELF+C │ SELF+C │ OWN*   │
│ customer            │ ✗      │ SELF   │ SELF   │ ✗      │
│ reseller_customer   │ ✗      │ SELF   │ SELF   │ ✗      │
└─────────────────────┴────────┴────────┴────────┴────────┘

Legend:
- ALL: All organizations
- SELF: Own organization only
- SELF+C: Self and own customers (resellers viewing their reseller_customers)
- OWN*: Own customers only (reseller creating/deleting reseller_customers)
- ✗: Not allowed

Endpoints:
- POST   /organizations/           - Create new organization
- GET    /organizations/           - List organizations (filtered by permissions)
- GET    /organizations/{id}       - Get specific organization
- PUT    /organizations/{id}       - Update organization
- DELETE /organizations/{id}       - Delete organization
"""

from uuid import UUID
from typing import Optional, Literal
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, Field

from app.core.db import Organization, User, get_db
from app.users import current_active_user
from app.api.dependencies import (
    get_user_organization, 
    PermissionChecker
)
from app.core.permit_service import (
    sync_organization_to_permit,
    check_permission
)


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

# Valid organization types - must match what's configured in Permit.io
OrganizationType = Literal["customer","assetwatch", "reseller", "reseller_customer"]


class OrganizationCreate(BaseModel):
    """
    Schema for creating a new organization.
    
    Fields:
    - organization_type: Determines permissions (assetwatch/reseller/customer/reseller_customer)
    - organization_name: Human-readable name for the organization
    - organization_email: Contact email (must be unique across all organizations)
    - parent_organization_id: Required for reseller_customer, null for others
    
    Business Rules:
    - Only one 'assetwatch' organization can exist (super admin)
    - 'reseller_customer' must have parent_organization_id pointing to a reseller
    - 'customer' and 'reseller' have null parent_organization_id
    """
    organization_type: OrganizationType
    organization_name: str = Field(..., min_length=1, max_length=255)
    organization_email: EmailStr
    parent_organization_id: Optional[UUID] = None


class OrganizationUpdate(BaseModel):
    """
    Schema for updating an organization.
    
    Only name and email can be updated.
    organization_type and parent_organization_id are immutable after creation.
    """
    organization_name: Optional[str] = Field(None, min_length=1, max_length=255)
    organization_email: Optional[EmailStr] = None


class OrganizationResponse(BaseModel):
    """
    Schema for organization in API responses.
    
    All fields are returned as strings for JSON serialization.
    """
    id: str
    organization_type: str
    organization_name: str
    organization_email: str
    parent_organization_id: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def org_to_response(org: Organization) -> dict:
    """
    Convert an Organization model to a response dictionary.
    
    This helper ensures consistent serialization of Organization objects.
    """
    return {
        "id": str(org.id),
        "organization_type": org.organization_type,
        "organization_name": org.organization_name,
        "organization_email": org.organization_email,
        "parent_organization_id": str(org.parent_organization_id) if org.parent_organization_id else None,
        "created_at": org.created_at.isoformat() if org.created_at else None,
        "updated_at": org.updated_at.isoformat() if org.updated_at else None
    }


# =============================================================================
# ROUTER
# =============================================================================

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    user_org: Optional[Organization] = Depends(get_user_organization)
):
    """
    Create a new organization.
    
    Authorization Rules:
    - assetwatch: Can create any organization type
    - reseller: Can only create 'reseller_customer' (their own customers)
    - customer/reseller_customer: Cannot create organizations
    
    Business Rules:
    - Only one 'assetwatch' organization can exist
    - 'reseller_customer' MUST have parent_organization_id (the reseller's ID)
    - Email must be unique across all organizations
    - When reseller creates reseller_customer, parent_organization_id auto-set to reseller's org
    
    Returns:
        The created organization
        
    Raises:
        403: If user doesn't have permission to create organizations
        400: If business rules are violated
    """
    print("-----------------------------------------------------------------")
    print(f"org_data--> {org_data}")
    print("current_active_user->>>>>>>", user.__dict__)
    print("user.email->>>>>>>", user.email)
    print("user.id->>>>>>>", user.id)
    print("user.organization_id->>>>>>>", user.organization_id)
    print("----------------------------------00000000000000000000000----")
    # Initialize permission checker with user and their organization
    checker = PermissionChecker(user, user_org)

    # Check basic create permission via Permit.io
    print("Check ----> ",await checker.can("create", "Organization"))
    if not await checker.can("create", "organization"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create organizations"
        )
    
    # === AUTHORIZATION LOGIC BASED ON ORG TYPE ===
    
    # AssetWatch (super admin) can create anything
    if checker.is_assetwatch():
        pass  # All good, proceed
    
    # Resellers can only create reseller_customer type
    elif checker.is_reseller():
        if org_data.organization_type != "reseller_customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Resellers can only create reseller_customer organizations"
            )
        # Auto-set parent to the reseller's organization
        # This ensures reseller_customers are always linked to their parent reseller
        org_data.parent_organization_id = user_org.id
    
    # Customers and reseller_customers cannot create organizations
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create organizations"
        )
    
    # === BUSINESS VALIDATION ===
    
    # Validate that reseller_customer has parent_organization_id
    if org_data.organization_type == "reseller_customer":
        if not org_data.parent_organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reseller_customer must have a parent_organization_id"
            )
        
        # Verify parent is actually a reseller
        parent_result = await db.execute(
            select(Organization).where(Organization.id == org_data.parent_organization_id)
        )
        parent = parent_result.scalars().first()
        
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent organization not found"
            )
        
        if parent.organization_type != "reseller":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent organization must be a reseller"
            )
    
    # Only one assetwatch organization can exist
    if org_data.organization_type == "assetwatch":
        existing_assetwatch = await db.execute(
            select(Organization).where(Organization.organization_type == "assetwatch")
        )
        if existing_assetwatch.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only one assetwatch organization can exist"
            )
    
    # Check email uniqueness
    existing_email = await db.execute(
        select(Organization).where(Organization.organization_email == org_data.organization_email)
    )
    if existing_email.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this email already exists"
        )
    
    # === CREATE ORGANIZATION ===
    
    db_org = Organization(
        organization_type=org_data.organization_type,
        organization_name=org_data.organization_name,
        organization_email=org_data.organization_email,
        parent_organization_id=org_data.parent_organization_id
    )
    
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    
    # Sync to Permit.io so it knows about this organization (tenant)
    await sync_organization_to_permit(
        organization_id=str(db_org.id),
        organization_type=db_org.organization_type,
        organization_name=db_org.organization_name
    )
    
    return org_to_response(db_org)

@router.post("/customer", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    user_org: Optional[Organization] = Depends(get_user_organization)
):
    """
    Create a new organization.
    
    Authorization Rules:
    - assetwatch: Can create any organization type
    - reseller: Can only create 'reseller_customer' (their own customers)
    - customer/reseller_customer: Cannot create organizations
    
    Business Rules:
    - Only one 'assetwatch' organization can exist
    - 'reseller_customer' MUST have parent_organization_id (the reseller's ID)
    - Email must be unique across all organizations
    - When reseller creates reseller_customer, parent_organization_id auto-set to reseller's org
    
    Returns:
        The created organization
        
    Raises:
        403: If user doesn't have permission to create organizations
        400: If business rules are violated
    """
    # Initialize permission checker with user and their organization
    checker = PermissionChecker(user, user_org)

    # Check basic create permission via Permit.io
    print("Check ----> ",await checker.can("create", "Organization"))
    if not await checker.can("create", "organization"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create organizations"
        )
    
    # === AUTHORIZATION LOGIC BASED ON ORG TYPE ===
    
    # Resellers can only create reseller_customer type
    elif checker.is_reseller():
        if org_data.organization_type != "reseller_customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Resellers can only create reseller_customer organizations"
            )
        # Auto-set parent to the reseller's organization
        # This ensures reseller_customers are always linked to their parent reseller
        org_data.parent_organization_id = user_org.id
    
    # Customers and reseller_customers cannot create organizations
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create organizations"
        )
    
    # === BUSINESS VALIDATION ===
    
    # Validate that reseller_customer has parent_organization_id
    if org_data.organization_type == "reseller_customer":
        if not org_data.parent_organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reseller_customer must have a parent_organization_id"
            )
        
        # Verify parent is actually a reseller
        parent_result = await db.execute(
            select(Organization).where(Organization.id == org_data.parent_organization_id)
        )
        parent = parent_result.scalars().first()
        
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent organization not found"
            )
        
        if parent.organization_type != "reseller":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent organization must be a reseller"
            )
    
    # Only one assetwatch organization can exist
    if org_data.organization_type == "assetwatch":
        existing_assetwatch = await db.execute(
            select(Organization).where(Organization.organization_type == "assetwatch")
        )
        if existing_assetwatch.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only one assetwatch organization can exist"
            )
    
    # Check email uniqueness
    existing_email = await db.execute(
        select(Organization).where(Organization.organization_email == org_data.organization_email)
    )
    if existing_email.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this email already exists"
        )
    
    # === CREATE ORGANIZATION ===
    
    db_org = Organization(
        organization_type=org_data.organization_type,
        organization_name=org_data.organization_name,
        organization_email=org_data.organization_email,
        parent_organization_id=org_data.parent_organization_id
    )
    
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    
    # Sync to Permit.io so it knows about this organization (tenant)
    await sync_organization_to_permit(
        organization_id=str(db_org.id),
        organization_type=db_org.organization_type,
        organization_name=db_org.organization_name
    )
    
    return org_to_response(db_org)


@router.get("/", response_model=list[OrganizationResponse])
async def list_organizations(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    user_org: Optional[Organization] = Depends(get_user_organization)
):
    """
    List organizations based on user's permissions.
    
    Returns different results based on user's organization type:
    - assetwatch: All organizations in the system
    - reseller: Self + own reseller_customers (children)
    - customer/reseller_customer: Self only
    
    Returns:
        List of organizations the user has access to
        
    Raises:
        403: If user doesn't belong to an organization
    """
    checker = PermissionChecker(user, user_org)
    
    # User must belong to an organization
    if not user_org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must belong to an organization"
        )
    
    # Build query based on organization type and permissions
    if checker.is_assetwatch():
        # AssetWatch sees ALL organizations
        result = await db.execute(
            select(Organization).order_by(Organization.created_at.desc())
        )
    elif checker.is_reseller():
        # Resellers see self + their reseller_customers (children)
        result = await db.execute(
            select(Organization)
            .where(
                (Organization.id == user_org.id) |  # Self
                (Organization.parent_organization_id == user_org.id)  # Children (reseller_customers)
            )
            .order_by(Organization.created_at.desc())
        )
    else:
        # Customers and reseller_customers see only themselves
        result = await db.execute(
            select(Organization).where(Organization.id == user_org.id)
        )
    
    orgs = result.scalars().all()
    
    return [org_to_response(org) for org in orgs]


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    user_org: Optional[Organization] = Depends(get_user_organization)
):
    """
    Get a specific organization by ID.
    
    Authorization:
    - assetwatch: Can view any organization
    - reseller: Can view self and own reseller_customers
    - customer/reseller_customer: Can only view self
    
    Returns:
        The requested organization
        
    Raises:
        403: If user doesn't have permission to view the organization
        404: If organization not found
    """
    checker = PermissionChecker(user, user_org)
    
    if not user_org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must belong to an organization"
        )
    
    # Fetch the organization
    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    org = result.scalars().first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check permission to view this organization
    can_view = False
    
    if checker.is_assetwatch():
        # AssetWatch can view any organization
        can_view = True
    elif checker.is_reseller():
        # Resellers can view self and their children
        can_view = (
            org.id == user_org.id or  # Self
            org.parent_organization_id == user_org.id  # Children
        )
    else:
        # Customers can only view self
        can_view = org.id == user_org.id
    
    if not can_view:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this organization"
        )
    
    return org_to_response(org)


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: UUID,
    org_update: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    user_org: Optional[Organization] = Depends(get_user_organization)
):
    """
    Update an organization.
    
    Authorization:
    - assetwatch: Can update any organization
    - reseller: Can update self and own reseller_customers
    - customer/reseller_customer: Can only update self
    
    Note: organization_type and parent_organization_id cannot be changed after creation.
    
    Returns:
        The updated organization
        
    Raises:
        403: If user doesn't have permission to update the organization
        404: If organization not found
        400: If email already exists
    """
    checker = PermissionChecker(user, user_org)
    
    if not user_org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must belong to an organization"
        )
    
    # Fetch the organization
    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    org = result.scalars().first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check permission to update this organization
    can_update = False
    
    if checker.is_assetwatch():
        # AssetWatch can update any organization
        can_update = True
    elif checker.is_reseller():
        # Resellers can update self and their children
        can_update = (
            org.id == user_org.id or  # Self
            org.parent_organization_id == user_org.id  # Children
        )
    else:
        # Customers can only update self
        can_update = org.id == user_org.id
    
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this organization"
        )
    
    # Check email uniqueness if being updated
    if org_update.organization_email and org_update.organization_email != org.organization_email:
        existing_email = await db.execute(
            select(Organization).where(
                Organization.organization_email == org_update.organization_email,
                Organization.id != org_id
            )
        )
        if existing_email.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization with this email already exists"
            )
    
    # Update fields (only those that were provided)
    update_data = org_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(org, key, value)
    
    await db.commit()
    await db.refresh(org)
    
    return org_to_response(org)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    user_org: Optional[Organization] = Depends(get_user_organization)
):
    """
    Delete an organization.
    
    Authorization:
    - assetwatch: Can delete any organization (except itself)
    - reseller: Can delete own reseller_customers only (not self)
    - customer/reseller_customer: Cannot delete organizations
    
    Warning: Deleting an organization will also delete all associated users and data.
    This action cannot be undone.
    
    Raises:
        403: If user doesn't have permission to delete the organization
        404: If organization not found
        400: If trying to delete own organization
    """
    checker = PermissionChecker(user, user_org)
    
    if not user_org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must belong to an organization"
        )
    
    # Fetch the organization to delete
    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    org = result.scalars().first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Prevent deleting your own organization
    if org_id == user_org.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own organization"
        )
    
    # Check permission to delete this organization
    can_delete = False
    
    if checker.is_assetwatch():
        # AssetWatch can delete any organization except itself (already checked above)
        can_delete = True
    elif checker.is_reseller():
        # Resellers can only delete their children (reseller_customers)
        can_delete = org.parent_organization_id == user_org.id
    else:
        # Customers cannot delete any organization
        can_delete = False
    
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this organization"
        )
    
    # Delete the organization
    # Note: This will cascade delete users and related data due to FK constraints
    await db.delete(org)
    await db.commit()
    
    # No content returned for DELETE
    return None
