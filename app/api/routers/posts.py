from fastapi import APIRouter, FastAPI, HTTPException, Depends, File, Form, UploadFile 
from sqlalchemy.ext.asyncio import AsyncSession
from app.images import imagekit
from app.core.db import Post, FilePost, User, create_db_and_tables, get_db
from sqlalchemy import select 
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users

router = APIRouter(prefix="/post", tags=["File_Posts"])


@router.post("/upload",tags=["upload file hahah"])
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form("") ,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
    ):
    # -------- upload image -------
    # create temp file
    temp_file_path= None
    print('file->', file)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            print('temp_file->', temp_file)
            print('temp_file.name->', temp_file.name)
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
            
            print("file>>", file)
        # Upload from file
        response = imagekit.files.upload(
            file=open(temp_file_path,"rb"),
            file_name=file.filename,
            folder="/products",
            tags=["product", "featured"]
        )
        print('response->', response) 
        # ---------------
    
        db_post = FilePost(
            user_id = user.id,
            caption = caption, 
            url = response.url,
            file_type = "video" if file.content_type.startswith("video/") else "image",
            file_name = response.name
        )
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post

    except Exception as e:
        print('e->', e)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        file.file.close() # we have to close this bcoz this is file FASTAPi open when it comes from FE

@router.get("/feed")
async def get_feed(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    result = await db.execute(select(FilePost).order_by(FilePost.created_at.desc()))
    posts = result.scalars().all()
        
    posts_data =[]
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                # "email": post.user.email #this is not working RN
            }
        )
        
    return {"posts": posts_data}

@router.delete("/posts/{post_id}")
async def delete_post(post_id: str,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(current_active_user),):
    try:
        post_uuid = uuid.UUID(post_id)
        
        result = await db.execute(select(FilePost).where(FilePost.id == post_uuid))
        post = result.scalars().first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, delete="You don't have permission to delete the post ")
        
        await db.delete(post)
        await db.commit()
        return {"success": True, "message": "Post deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except Exception as e:
        print('e->', e)
        raise HTTPException(status_code=500, detail=str(e))
    