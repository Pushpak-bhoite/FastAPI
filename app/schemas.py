from pydantic import BaseModel #this is a object 
from datetime import date
from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
    title:str
    content: str
    caption: str

class PostResponse(BaseModel):
    id: int
    title:str
    content: str
    caption: str

    class Config: 
        from_attributes = True # this is for returning id along with data when user makes post request

class FilePost(BaseModel):
    id: int
    caption:str
    file_url: str
    file_name: str
    created_At: date
    class Config: 
        from_attributes = True 
        
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class AssetCreate(BaseModel):
    name: str
    asset_type: str  # "http" | "ssl" | "ping" | "port" | "dns"
    target: str  # URL / domain / IP
    port: int | None = None

class AssetResponse(BaseModel):
    id: str
    name: str
    asset_type: str
    target: str
    port: int | None
    status: str  # "up", "down", "unknown"
    last_checked_at: str | None
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class AssetUpdate(BaseModel):
    name: str | None = None
    target: str | None = None
    port: int | None = None
    asset_type: str | None = None