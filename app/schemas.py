from pydantic import BaseModel #this is a object 

class PostCreate(BaseModel):
    title:str
    content: str

class PostResponse(BaseModel):
    title:str
    content: str