import pydantic
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id:int = Field(..., description="User's id",)
    created_at:int
    level:str
    name:str
    description:str
    posts:list[int]
    comments:list[int]

class Image(BaseModel):
    id:int
    uri:str
    height:int
    width:int
    mimetype:str

class Tag(BaseModel):
    name:str
    created_at:int
    namespace:str
    count:int|None = None

class Post(BaseModel):
    id:int
    creator:int
    created_at:int
    md5:list[str]
    sha256:list[str]
    language:str
    source:str
    rating:str
    type:str
    sound:bool
    
    views:int
    upvotes:int
    downvotes:int
    
    full:Image
    preview:Image
    thumbnail:Image
    
    tags:list[str]
    'example: "generic:text"'
    comments:list[int]

class Profile(User):
    email:str
    settings:dict
    history:list[int]
    favourites:list[int]
    blocked:list[int]

class Comment(BaseModel):
    id:int
    created_at:int
    creator:int
    text:str
    post:int|None = None
    report:int|None = None

class Report(BaseModel):
    id:int
    creator:int
    created_at:int
    title:str
    messages:list[str]
