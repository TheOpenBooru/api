from dataclasses import dataclass

@dataclass()
class User:
    id:int
    created_at:int
    level:str
    name:str
    description:str
    posts:list[int]
    comments:list[int]

    email:str
    settings:dict
    
    history:list[int]
    favourites:list[int]
    blocked:list[int]
    upvotes:list[int]
    downvotes:list[int]

@dataclass()
class Image:
    id:int
    url:str
    height:int
    width:int
    mimetype:str

@dataclass()
class Tag:
    name:str
    created_at:int
    namespace:str
    count:int

@dataclass()
class Post:
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
    
    full:int
    preview:int
    thumbnail:int
    
    tags:list[str]
    comments:list[int]


@dataclass()
class Comment:
    id:int
    created_at:int
    creator:int
    text:str
    post:int
