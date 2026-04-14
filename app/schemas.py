from pydantic import BaseModel #this is a object 
from datetime import date

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
