from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, get_db
from database import Base
from models.items import Todo, TodoCreate, TodoResponse
app = FastAPI()

items = list()

Base.metadata.create_all(bind=engine)   #this is for db connection
class Item(BaseModel):
    item: str = Field(..., min_length=3, max_length=30)
    

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items", response_model=TodoResponse)
def get_all_items(todo: TodoCreate, db: Session = Depends(get_db)): #Session = Depends why both from different libs.    
    return {"items":items}

@app.get("/items/{item_id}", response_model=TodoResponse)
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/item")
def create_item(todo: TodoCreate, db: Session = Depends(get_db)): #Session is just a type hint provided by sqlAlchemy
    db_todo = Todo(title=todo.title, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return {"message": "Item created successfully", "items":db_todo}

@app.patch("/item/{id}")
def update_item(id: int, item: Item):
    items[id] = item
    return {"items":items}