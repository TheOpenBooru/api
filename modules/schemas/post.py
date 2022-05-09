from . import fields,BaseModel,GenericMedia,Image
from pydantic import Field
import time


class Post_Edit(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At
    editter: int = fields.User_ID
    tags: list[str] = fields.Tags

class Post_Query(BaseModel):
    index: int = Field(default=0, description="Offset from the start of the results")
    limit: int = Field(default=64, description="Maximum number of results to return")
    sort: str = Field(default="created_at", description="How to sort the posts")
    descending: bool = Field(default=True, description="Should search be ordered descending")
    
    include_tags: list[str] = fields.Tags
    exclude_tags: list[str] = fields.Tags
    
    created_after:float|None = Field(default=None)
    created_before:float|None = Field(default=None)
    
    md5:str|None = Field(default_factory=list)
    sha256:str|None = Field(default_factory=list)


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
