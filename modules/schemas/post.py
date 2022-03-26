from . import fields
from . import Image,Video,Animation,GenericMedia
from pydantic import BaseModel, Field, AnyHttpUrl


class Post_Edit(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At
    editter: int = fields.User_ID
    tags: list[str] = fields.Tags

class Post(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At
    uploader: int = fields.User_ID
    deleted: bool = Field(default=False, description="Whether the post has been deleted")

    full: GenericMedia = Field(..., description="The full scale media for the Post")
    preview: GenericMedia|None = Field(default=None,description="A Medium Scale Version for the image, for hi-res posts")
    thumbnail: Image = Field(..., description="The lowest scale version of the image, for thumbnails")
    
    md5s: list[str] = Field(default_factory=list, description="The Post's MD5 hashes")
    sha256s: list[str] = Field(default_factory=list, description="The Post's SHA3-256 hashes")
    media_type: str = fields.Post_Type
    
    tags: list[str] = fields.Tags
    comments: list[int] = fields.Comments

    views: int = Field(default=0, description="Number of views on the Post")
    upvotes: int = Field(default=0, description="Number of upvotes on the Post")
    downvotes: int = Field(default=0, description="Number of downvotes on the Post")
