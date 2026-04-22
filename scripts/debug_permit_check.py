"""
Debug script to check why permission is denied.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.core.permit_service import permit


async def debug_permission():
    user_id = "6556b99d-6abf-4be3-b2fc-01065f98ec6f"
    tenant_id = "4c48e59d-77bc-4f6f-9d92-0f09a64eeea0"
    
    print("\n" + "=" * 70)
    print("          PERMIT.IO DEBUG")
    print("=" * 70)
    
    # 1. Check if tenant exists
    print("\n1️⃣  CHECKING TENANT...")
    try:
        tenant = await permit.api.tenants.get(tenant_id)
        print(f"   ✅ Tenant exists: {tenant.key}")
        print(f"      Name: {tenant.name}")
        print(f"      Attributes: {getattr(tenant, 'attributes', {})}")
    except Exception as e:
        print(f"   ❌ Tenant NOT found: {e}")
        print("   👉 Need to sync organization to Permit.io!")
    
    # 2. Check if user exists
    print("\n2️⃣  CHECKING USER...")
    try:
        user = await permit.api.users.get(user_id)
        print(f"   ✅ User exists: {user.key}")
        print(f"      Email: {getattr(user, 'email', 'N/A')}")
    except Exception as e:
        print(f"   ❌ User NOT found: {e}")
        print("   👉 Need to sync user to Permit.io!")
    
    # 3. Check user's role assignments
    print("\n3️⃣  CHECKING ROLE ASSIGNMENTS...")
    try:
        roles = await permit.api.users.get_assigned_roles(user_id)
        if roles:
            print(f"   ✅ User has {len(roles)} role(s):")
            for role in roles:
                print(f"      - Role: {role.role} in Tenant: {role.tenant}")
        else:
            print("   ❌ User has NO roles assigned!")
            print("   👉 Need to assign role to user in tenant!")
    except Exception as e:
        print(f"   ❌ Error getting roles: {e}")
    
    # 4. Check if role exists
    print("\n4️⃣  CHECKING ROLES IN PERMIT.IO...")
    try:
        all_roles = await permit.api.roles.list()
        print(f"   Available roles:")
        for role in all_roles:
            print(f"      - {role.key}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Check if resource exists
    print("\n5️⃣  CHECKING RESOURCES IN PERMIT.IO...")
    try:
        resources = await permit.api.resources.list()
        print(f"   Available resources:")
        for res in resources:
            actions = getattr(res, 'actions', {})
            print(f"      - {res.key}: {list(actions.keys()) if actions else 'no actions'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Try the actual permission check
    print("\n6️⃣  TESTING PERMISSION CHECK...")
    try:
        allowed = await permit.check(
            user_id,
            "create",
            {"type": "organization", "tenant": tenant_id}
        )
        print(f"   Result: {'✅ ALLOWED' if allowed else '❌ DENIED'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("          DIAGNOSIS")
    print("=" * 70)
    print("""
    If permission is denied, check:
    
    1. Does the user exist in Permit.io?
       → Run: sync_user_to_permit(user_id, email, tenant_id, "assetwatch")
    
    2. Does the user have a role in the tenant?
       → Run: assign_role(user_id, "assetwatch", tenant_id)
    
    3. Does the role have permission to create organization?
       → Go to Permit.io Dashboard → Policy → Permissions
       → Enable "create" on "organization" for "assetwatch" role
    """)


if __name__ == "__main__":
    asyncio.run(debug_permission())