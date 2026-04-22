# Permit.io Setup Guide for AssetWatch

This guide walks you through setting up Permit.io for the AssetWatch authorization system.

## Overview

Permit.io handles authorization (who can do what) for the AssetWatch system. The integration works like this:

1. **Your App** → Creates users/organizations → **Syncs to Permit.io**
2. **Your App** → Checks permission → **Asks Permit.io** → Returns allow/deny
3. **Permit.io Dashboard** → Configure roles & permissions

## Step 1: Create Permit.io Account

1. Go to [app.permit.io](https://app.permit.io) and sign up
2. Create a new project called "AssetWatch"
3. You'll start in the "Development" environment

## Step 2: Get Your API Key

1. Go to **Settings** (gear icon) → **API Keys**
2. Copy the **Environment API Key** (starts with `permit_key_`)
3. Create a `.env` file in your project root:

```bash
PERMIT_IO_KEY=permit_key_your_key_here
```

## Step 3: Create Resources

Resources are the things you want to protect. Go to **Policy → Resources** and create:

### Resource 1: `organization`
- **Key**: `organization`
- **Name**: Organization
- **Actions**: 
  - `create` - Create new organizations
  - `read` - View organization details
  - `update` - Modify organization
  - `delete` - Remove organization

### Resource 2: `asset`
- **Key**: `asset`
- **Name**: Asset
- **Actions**: `create`, `read`, `update`, `delete`

### Resource 3: `monitor`
- **Key**: `monitor`
- **Name**: Monitor
- **Actions**: `create`, `read`, `update`, `delete`

## Step 4: Create Roles

Roles define permission sets. Go to **Policy → Roles** and create:

| Role Key | Role Name | Description |
|----------|-----------|-------------|
| `assetwatch` | AssetWatch Admin | Super admin - full access |
| `reseller` | Reseller | Can manage own customers |
| `customer` | Customer | Direct customer |
| `reseller_customer` | Reseller Customer | Customer of a reseller |

## Step 5: Configure Permissions

Go to **Policy → Policy Editor** and set permissions for each role:

### `assetwatch` (Super Admin)
| Resource | create | read | update | delete |
|----------|--------|------|--------|--------|
| organization | ✅ | ✅ | ✅ | ✅ |
| asset | ✅ | ✅ | ✅ | ✅ |
| monitor | ✅ | ✅ | ✅ | ✅ |

### `reseller`
| Resource | create | read | update | delete |
|----------|--------|------|--------|--------|
| organization | ✅ | ✅ | ✅ | ✅ |
| asset | ✅ | ✅ | ✅ | ✅ |
| monitor | ✅ | ✅ | ✅ | ✅ |

> Note: Additional filtering (reseller can only manage their own customers) is handled in the FastAPI code.

### `customer`
| Resource | create | read | update | delete |
|----------|--------|------|--------|--------|
| organization | ❌ | ✅ | ✅ | ❌ |
| asset | ✅ | ✅ | ✅ | ✅ |
| monitor | ✅ | ✅ | ✅ | ✅ |

### `reseller_customer`
| Resource | create | read | update | delete |
|----------|--------|------|--------|--------|
| organization | ❌ | ✅ | ✅ | ❌ |
| asset | ✅ | ✅ | ✅ | ✅ |
| monitor | ✅ | ✅ | ✅ | ✅ |

## Step 6: Initialize Your Database

Run the setup script to create the initial AssetWatch organization:

```bash
# Make sure you have PERMIT_IO_KEY in .env
source .venv/bin/activate
python scripts/setup_initial_org.py
```

## Step 7: Create Your First Admin User

1. Start your FastAPI server:
```bash
uvicorn app.app:app --reload
```

2. Register a user via the API:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@assetwatch.com",
    "password": "securepassword123"
  }'
```

3. Assign the user to AssetWatch organization:
```bash
python scripts/setup_initial_org.py --assign-user admin@assetwatch.com
```

## API Usage Examples

### Login
```bash
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@assetwatch.com&password=securepassword123"
```

Save the token from the response.

### Create a Reseller (as AssetWatch admin)
```bash
curl -X POST "http://localhost:8000/api/organizations/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_type": "reseller",
    "organization_name": "Acme Reseller",
    "organization_email": "contact@acme.com"
  }'
```

### Create a Customer for Reseller
```bash
curl -X POST "http://localhost:8000/api/organizations/" \
  -H "Authorization: Bearer RESELLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_type": "reseller_customer",
    "organization_name": "Small Business Inc",
    "organization_email": "info@smallbiz.com"
  }'
```

### List Organizations
```bash
curl "http://localhost:8000/api/organizations/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Permission Matrix

| Role | Create Org | Read Org | Update Org | Delete Org |
|------|------------|----------|------------|------------|
| assetwatch | ALL types | ALL | ALL | ALL (except self) |
| reseller | reseller_customer only | Self + children | Self + children | Children only |
| customer | ❌ | Self only | Self only | ❌ |
| reseller_customer | ❌ | Self only | Self only | ❌ |

## Troubleshooting

### "Permission denied" errors
1. Check that the user is synced to Permit.io (check logs for "✅ User synced")
2. Verify the role is assigned in Permit.io dashboard
3. Check that the organization (tenant) exists in Permit.io

### Users not syncing
1. Verify `PERMIT_IO_KEY` is set correctly in `.env`
2. Check the console for sync error messages
3. Ensure you're using the Development environment key

### Check Permit.io Audit Logs
Go to **Audit Logs** in Permit.io dashboard to see all permission checks and their results.

## Files Created

| File | Purpose |
|------|---------|
| `app/core/permit_service.py` | Permit.io client and helper functions |
| `app/core/db.py` | Organization model added |
| `app/api/dependencies.py` | Authorization dependencies |
| `app/api/routers/organizations.py` | Organization CRUD endpoints |
| `scripts/setup_initial_org.py` | Initial setup script |

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   FastAPI App   │ ←sync→  │   Permit.io     │
│                 │         │                 │
│ ┌─────────────┐ │         │ ┌─────────────┐ │
│ │   Users     │─┼─────────┼→│   Users     │ │
│ └─────────────┘ │         │ └─────────────┘ │
│                 │         │                 │
│ ┌─────────────┐ │         │ ┌─────────────┐ │
│ │Organizations│─┼─────────┼→│  Tenants    │ │
│ └─────────────┘ │         │ └─────────────┘ │
│                 │         │                 │
│ check_permission│─────────┼→│ Policy Check │ │
└─────────────────┘         └─────────────────┘
```
