from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.schemas import PostCreate, PostResponse

app = FastAPI()

text_posts = {
    1: {"id": 1, "title": "Post 1", "content": "Content of post 1"},
    2: {"id": 2, "title": "Post 2", "content": "Content of post 2"},
    3: {"id": 3, "title": "Post 3", "content": "Content of post 3"},
    4: {"id": 4, "title": "Post 4", "content": "Content of post 4"},
    5: {"id": 5, "title": "Post 5", "content": "Content of post 5"},
    6: {"id": 6, "title": "Post 6", "content": "Content of post 6"},
    7: {"id": 7, "title": "Post 7", "content": "Content of post 7"},
    8: {"id": 8, "title": "Post 8", "content": "Content of post 8"},
    9: {"id": 9, "title": "Post 9", "content": "Content of post 9"},
    10: {"id": 10, "title": "Post 10", "content": "Content of post 10"},
}

@app.get("/")
def hello_world_function():
    return {"message":"Hello World"}

@app.get("/hello")
def my_function_2():
    return {"message":"Hello World"}; 

@app.get("/posts")
def get_all_posts(limit: int = None):   # This limit is query param -> ?limit=3
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts #if no limit then return all posts 
# get specific doc
@app.get("/post/{id}")
def get_post(id:int):
    if id not in text_posts:
        raise HTTPException(status=404, detail="post not found" )
    return text_posts.get(id)

@app.post("/posts")  #mention return type
def create_post(post: PostCreate)-> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post


# # Create a new post
# @app.post("/posts", response_model=PostResponse, status_code=201)
# def create_post(post: PostCreate, db: Session = Depends(get_db)): ### im trying to add caption field here
#     db_post = Post(title=post.title, content=post.content, caption=post.caption)
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post

# # Get all posts
# @app.get("/posts", response_model=PostResponse)
# def get_all_posts(db: Session = Depends(get_db)):
#     posts = db.query(Post).all()
#     return posts

# # Get a specific post by ID
# @app.get("/post/{id}")
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(Post).filter(Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return post

# @app.delete("/post/{id}", status_code=204)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(Post).filter(Post.id == id).first()
#     if not post:
#          raise HTTPException(status=404, detail="Post not found")
#     db.delete(post)
#     db.commit()
#     return {"message": "Post deleted successfully"}
    
### Code with images 
# Create a new post

