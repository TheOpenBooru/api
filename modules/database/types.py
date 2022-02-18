from dataclasses import dataclass,field
import logging
from modules import schemas

class Default:
    id:int
    created_at:int
    def to_pydantic(self):
        raise NotImplementedError
    def from_pydantic(self):
        raise NotImplementedError

@dataclass
class User(Default):
    id:int
    created_at:int
    level:str
    name:str
    email:str
    bio:str = ""
    settings:str = ""
    posts:list[int] = field(default_factory=list)
    comments:list[int] = field(default_factory=list)
    
    history:list[int] = field(default_factory=list)
    favourites:list[int] = field(default_factory=list)
    blocked:list[int] = field(default_factory=list)
    upvotes:list[int] = field(default_factory=list)
    downvotes:list[int] = field(default_factory=list)
    def to_pydantic(self) -> schemas.User:
        return schemas.User.from_orm(self)


@dataclass
class Image:
    url:str
    height:int
    width:int
    mimetype:str
    def to_pydantic(self) -> schemas.Image:
        return schemas.Image(
            url=self.url,mimetype=self.mimetype,
            height=self.height,width=self.width
        )


@dataclass
class Tag(Default):
    name:str
    created_at:int
    namespace:str='generic'
    count:int=0
    def to_pydantic(self) -> schemas.Tag:
        return schemas.Tag.from_orm(self)


@dataclass
class Post(Default):
    id:int
    creator:int
    created_at:int
    md5s:list[str] 
    sha256s:list[str]
    type:str
    sound:bool
    
    full:Image
    thumbnail:Image|None = None
    preview:Image|None = None
    
    language:str|None = None
    rating:str|None = None
    source:None = None
    
    views:int = 0
    upvotes:int = 0
    downvotes:int = 0
    
    tags:list[str] = field(default_factory=list)
    comments:list[int] = field(default_factory=list)
    def to_pydantic(self) -> schemas.Post:
        return schemas.Post(
            id=self.id,
            created_at=self.created_at,
            sha256s=self.sha256s,md5s=self.md5s,
            type=self.type,
            sound=self.sound,
            full=self.full.to_pydantic(),
            thumbnail=self.thumbnail.to_pydantic(),
            preview=self.preview.to_pydantic() if self.preview else None,
            language=self.language,
            age_rating=self.rating,
            source=None,
            views=self.views,
            upvotes=self.upvotes,
            downvotes=self.downvotes,
            tags=self.tags,
            comments=self.comments,
        )
