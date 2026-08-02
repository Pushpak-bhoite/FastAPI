from pydantic import BaseModel, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    completed: Mapped[bool] = mapped_column(default=False)
    
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False
    
class TodoResponse(BaseModel):
    id: int 
    title: str
    completed: bool
    
    model_config = {"from_attributes": True }  ##### use of this line
    