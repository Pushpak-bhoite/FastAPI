"""
Permit.io Setup Script

Run this script after setting up Permit.io dashboard to create the initial
AssetWatch organization and admin user.

Usage:
    1. First, configure Permit.io dashboard (see PERMIT_SETUP.md)
    2. Create a .env file with PERMIT_IO_KEY
    3. Run: python scripts/setup_initial_org.py

This will:
    1. Create the 'assetwatch' organization (super admin)
    2. Sync it to Permit.io
    3. Optionally assign an existing user to it
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.core.db import Organization, User, async_session_maker, create_db_and_tables
from app.core.permit_service import sync_organization_to_permit, sync_user_to_permit
from sqlalchemy import select


async def setup_assetwatch_organization():
    """
    Create the initial AssetWatch organization if it doesn't exist.
    
    AssetWatch is the super admin organization that manages all other
    organizations, resellers, and customers.
    """
    print("🚀 Setting up AssetWatch organization...")
    
    # Create tables if they don't exist
    await create_db_and_tables()
    print("✅ Database tables created/verified")
    
    async with async_session_maker() as session:
        # this code wont let u create new assetwatch user
        # Check if assetwatch org already exists
        result = await session.execute(
            select(Organization).where(Organization.organization_type == "assetwatch")
        )
        existing = result.scalars().first()
        
        if existing:
            print(f"ℹ️ AssetWatch organization already exists: {existing.organization_name}")
            return existing
        
        # Create the assetwatch organization
        assetwatch_org = Organization(
            organization_type="assetwatch",
            organization_name="AssetWatch",
            organization_email="bran@assetwatch.com",
            parent_organization_id=None
        )
        print("Org->>>",assetwatch_org)
        session.add(assetwatch_org)
        await session.commit()
        await session.refresh(assetwatch_org)
        
        print(f"✅ Created AssetWatch organization: {assetwatch_org.id}")
        
        # Sync to Permit.io
        await sync_organization_to_permit(
            organization_id=str(assetwatch_org.id),
            organization_type="assetwatch",
            organization_name="AssetWatch"
        )
        
        return assetwatch_org


async def assign_user_to_assetwatch(user_email: str):
    """
    Assign an existing user to the AssetWatch organization.
    
    This gives the user super admin permissions.
    """
    async with async_session_maker() as session:
        # Find the user
        result = await session.execute(
            select(User).where(User.email == user_email)
        )
        user = result.scalars().first()
        
        if not user:
            print(f"❌ User with email {user_email} not found")
            return None
        
        # Find assetwatch org
        result = await session.execute(
            select(Organization).where(Organization.organization_type == "assetwatch")
        )
        org = result.scalars().first()
        
        if not org:
            print("❌ AssetWatch organization not found. Run setup first.")
            return None
        
        # Assign user to organization
        user.organization_id = org.id
        await session.commit()
        
        print(f"✅ Assigned user {user_email} to AssetWatch organization")
        
        # Sync to Permit.io
        await sync_user_to_permit(
            user_id=str(user.id),
            email=user.email,
            organization_id=str(org.id),
            organization_type="assetwatch"
        )
        
        return user


async def main():
    print("=" * 60)
    print("Permit.io Initial Setup")
    print("=" * 60)
    
    # Check for API key
    if not os.environ.get("PERMIT_IO_KEY"):
        print("⚠️ Warning: PERMIT_IO_KEY not set in environment")
        print("   Permit.io sync will fail. Set it in .env file.")
        print()
    
    # Check for --assign-user flag (skip org creation if just assigning)
    if len(sys.argv) > 2 and sys.argv[1] == "--assign-user":
        user_email = sys.argv[2]
        await assign_user_to_assetwatch(user_email)
        return
    
    # Create assetwatch organization
    org = await setup_assetwatch_organization()
    
    print()
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Register a user via the API (POST /auth/register)")
    print("2. Run this script with --assign-user flag to make them admin:")
    print("   python scripts/setup_initial_org.py --assign-user bran@assetwatch.com")
    print()


if __name__ == "__main__":
    asyncio.run(main())
