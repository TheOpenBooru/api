from dataclasses import dataclass
from modules import types

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
    def to_profile(self) -> types.Profile:
        return types.Profile(
            id=self.id,created_at=self.created_at,
            level=self.level,name=self.name,
            description=self.description,
            posts=self.posts,comments=self.comments,
            email=self.email,settings=self.settings,
            history=self.history,
            favourites=self.favourites,
            blocked=self.blocked
        )
    def to_user(self) -> types.User:
        return types.User(
            id=self.id,created_at=self.created_at,
            level=self.level,name=self.name,
            description=self.description,
            posts=self.posts,comments=self.comments
        )

@dataclass()
class Image:
    url:str
    height:int
    width:int
    mimetype:str
    def to_pydantic(self) -> types.Image:
        return types.Image(
            uri=self.url,mimetype=self.mimetype,
            height=self.height,width=self.width
        )

@dataclass(kw_only=False)
class Tag:
    name:str
    created_at:int
    namespace:str
    count:int
    def to_pydantic(self) -> types.Tag:
        return types.Tag(
            name=self.name,created_at=self.created_at,
            namespace=self.namespace,count=self.count
        )

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
    
    full:Image
    preview:Image
    thumbnail:Image
    
    tags:list[str]
    comments:list[int]
    def to_pydantic(self) -> types.Post:
        return types.Post(
            id=self.id,created_at=self.created_at,
            creator=self.creator,source=self.source,
            md5=self.md5,sha256=self.sha256,
            type=self.type,sound=self.sound,
            rating=self.rating,language=self.language,
            downvotes=self.downvotes,upvotes=self.upvotes,
            full=self.full.to_pydantic(),
            preview=self.preview.to_pydantic(),
            thumbnail=self.thumbnail.to_pydantic(),
            views=self.views,tags=self.tags,comments=self.comments
            )


@dataclass()
class Comment:
    id:int
    created_at:int
    creator:int
    text:str
    post:int
    def to_pydantic(self) -> types.Comment:
        return types.Comment(
            id=self.id,created_at=self.created_at,
            creator=self.creator,text=self.text,
            post=self.post
            )
