from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import Asset, User, get_db
from app.users import current_active_user
from app.schemas import AssetCreate, AssetResponse, AssetUpdate
from datetime import datetime
import httpx
import socket

router = APIRouter(prefix="/assets", tags=["assets"])

# Helper function to check asset status
async def check_asset_status(asset_type: str, target: str, port: int | None = None) -> str:
    try:
        if asset_type == "http":
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"http://{target}")
                return "up" if response.status_code < 500 else "down"
        
        elif asset_type == "ping":
            # Simple TCP connection check
            try:
                socket.create_connection((target, 80), timeout=2)
                return "up"
            except:
                return "down"
        
        elif asset_type == "port":
            if not port:
                return "unknown"
            try:
                socket.create_connection((target, port), timeout=2)
                return "up"
            except:
                return "down"
        
        elif asset_type == "dns":
            try:
                socket.gethostbyname(target)
                return "up"
            except:
                return "down"
        
        return "unknown"
    except Exception as e:
        print(f"Error checking asset: {e}")
        return "down"

# Create asset
@router.post("/", response_model=AssetResponse, status_code=201)
async def create_asset(
    asset: AssetCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    db_asset = Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        target=asset.target,
        port=asset.port,
        user_id=user.id
    )
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    
    return {
        "id": str(db_asset.id),
        "name": db_asset.name,
        "asset_type": db_asset.asset_type,
        "target": db_asset.target,
        "port": db_asset.port,
        "status": db_asset.status,
        "last_checked_at": None,
        "created_at": db_asset.created_at.isoformat(),
        "updated_at": db_asset.updated_at.isoformat()
    }

# Get all assets for user
@router.get("/", response_model=list[AssetResponse])
async def get_all_assets(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    result = await db.execute(select(Asset).where(Asset.user_id == user.id))
    assets = result.scalars().all()
    
    return [
        {
            "id": str(asset.id),
            "name": asset.name,
            "asset_type": asset.asset_type,
            "target": asset.target,
            "port": asset.port,
            "status": asset.status,
            "last_checked_at": asset.last_checked_at.isoformat() if asset.last_checked_at else None,
            "created_at": asset.created_at.isoformat(),
            "updated_at": asset.updated_at.isoformat()
        }
        for asset in assets
    ]

# Get single asset
@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    result = await db.execute(
        select(Asset).where(Asset.id == asset_id, Asset.user_id == user.id)
    )
    asset = result.scalars().first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return {
        "id": str(asset.id),
        "name": asset.name,
        "asset_type": asset.asset_type,
        "target": asset.target,
        "port": asset.port,
        "status": asset.status,
        "last_checked_at": asset.last_checked_at.isoformat() if asset.last_checked_at else None,
        "created_at": asset.created_at.isoformat(),
        "updated_at": asset.updated_at.isoformat()
    }

# Update asset
@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    asset_update: AssetUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    result = await db.execute(
        select(Asset).where(Asset.id == asset_id, Asset.user_id == user.id)
    )
    asset = result.scalars().first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)
    
    await db.commit()
    await db.refresh(asset)
    
    return {
        "id": str(asset.id),
        "name": asset.name,
        "asset_type": asset.asset_type,
        "target": asset.target,
        "port": asset.port,
        "status": asset.status,
        "last_checked_at": asset.last_checked_at.isoformat() if asset.last_checked_at else None,
        "created_at": asset.created_at.isoformat(),
        "updated_at": asset.updated_at.isoformat()
    }

# Delete asset
@router.delete("/{asset_id}", status_code=204)
async def delete_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    result = await db.execute(
        select(Asset).where(Asset.id == asset_id, Asset.user_id == user.id)
    )
    asset = result.scalars().first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    await db.delete(asset)
    await db.commit()

# Check/Monitor single asset
@router.post("/{asset_id}/check")
async def check_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    result = await db.execute(
        select(Asset).where(Asset.id == asset_id, Asset.user_id == user.id)
    )
    asset = result.scalars().first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    status = await check_asset_status(asset.asset_type, asset.target, asset.port)
    
    asset.status = status
    asset.last_checked_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(asset)
    
    return {
        "id": str(asset.id),
        "status": asset.status,
        "last_checked_at": asset.last_checked_at.isoformat()
    }
