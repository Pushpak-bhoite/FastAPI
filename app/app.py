from fastapi import FastAPI, HTTPException, Depends, File, Form, UploadFile 
from sqlalchemy.orm import Session  #sqlalchemy is orm it let's us write db methods rather than sql queries 
from app.schemas import PostCreate, PostResponse
from app.db import Post, FilePost, get_db
FilePost
from sqlalchemy import select 
import shutil
import os
import uuid
import tempfile
from imagekitio import ImageKit
from app.images import imagekit

app = FastAPI()

@app.get("/")
def hello_world_function():
    return {"message":"Hello World"}

# Create a new post
@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)): ### im trying to add caption field here
    db_post = Post(title=post.title, content=post.content, caption=post.caption)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Get all posts
@app.get("/posts", response_model=PostResponse)
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

# Get a specific post by ID
@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/post/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
         raise HTTPException(status=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
    

# Create a new post
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form("") ,
    db: Session = Depends(get_db)
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
            print(f"File properties:")
            print(f"Filename: {file.filename}")
            print(f"Content type: {file.content_type}")
            print(f"Size: {file.size}")
            print("file>>", file)
        # Upload from file
        response = imagekit.files.upload(
            file=open(temp_file_path,"rb"),
            file_name=file.filename,
            folder="/products",
            tags=["product", "featured"]
        )
        print(f"File ID: {response.file_id}")
        print(f"URL: {response.url}")
        
        # ---------------
    
        db_post = FilePost(
            caption=caption, 
            url=response.url,
            file_type="photo",
            file_name="dummy name"
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    except Exception as e:
        print('e->', e)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/feed")
async def get_feed(
    db: Session = Depends(get_db)
):
    # result =  db.execute(select(FilePost).order_by(FilePost.created_At.desc())) # this code will work with async await
    # posts = [row[0] for row in result.all()]
    posts = db.query(FilePost).order_by(FilePost.created_At.desc()).all()
        
    posts_data =[]
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_At": post.created_At.isoformat(),
            }
        )
        
    return {"posts": posts_data}