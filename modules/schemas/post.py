from . import fields
from . import Image,Video,Animation
from pydantic import BaseModel, Field, AnyHttpUrl


class Post_Edit(BaseModel):
    removed_tags: list[str] = fields.Tags
    added_tags: list[str] = fields.Tags
    
    from_language: str|None = fields.Lanugage
    to_language: str = fields.Lanugage
    
    from_age_rating: str|None = fields.Age_Rating
    to_age_rating: str = fields.Age_Rating
    
    from_source:AnyHttpUrl|None = fields.Source
    to_source:AnyHttpUrl = fields.Source

class Post(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At
    uploader: int = fields.User_ID
    deleted: bool = Field(default=False, description="Whether the post has been deleted")

    full: Image|Video|Animation = fields.Full_Image
    preview: Image|Video|None = fields.Preview_Image
    thumbnail: Image = fields.Thumbnail_Image
    
    md5s: list[str] = Field(default_factory=list, description="The Post's MD5 hashes")
    sha256s: list[str] = Field(default_factory=list, description="The Post's SHA3-256 hashes")
    type: str = fields.Post_Type
    
    language: str|None   = fields.Lanugage
    age_rating: str|None = fields.Age_Rating
    source: AnyHttpUrl|None = fields.Source

    tags: list[str] = fields.Tags
    comments: list[int] = fields.Comments

    views: int = Field(default=0, description="Number of views on the Post")
    upvotes: int = Field(default=0, description="Number of upvotes on the Post")
    downvotes: int = Field(default=0, description="Number of downvotes on the Post")
