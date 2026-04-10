from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import PostCreate, PostResponse
from app.db import Post, get_db

app = FastAPI()

@app.get("/")
def hello_world_function():
    return {"message":"Hello World"}

# Create a new post
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)): ### im trying to add caption field ehere
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Get all posts
@app.get("/posts")
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