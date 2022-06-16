from . import fields,BaseModel,GenericMedia,Image
from modules import settings,validate
from pydantic import Field
from typing import Union
from enum import Enum


class PostEdit(BaseModel):
    created_at: float = fields.Created_At
    post_id: int = fields.Item_ID
    editter_id: int = fields.Item_ID
    
    old_tags: list[str] = fields.Tags
    new_tags: list[str] = fields.Tags
    old_source: str = Field(default="", description="The previous source for the post")
    new_source: str = Field(default="", description="The new source for the post")


class Valid_Post_Sorts(str, Enum):
    id = "id"
    created_at = "created_at"
    upvotes = "upvotes"
    downvotes = "downvotes"


class Post_Query(BaseModel):
    index: int = Field(default=0, description="Offset from the start of the results")
    limit: int = Field(default=64, description="Maximum number of results to return")
    sort: Valid_Post_Sorts = Field(default=settings.POSTS_SEARCH_DEFAULT_SORT, description="How to sort the posts")
    descending: bool = Field(default=True, description="Should search be ordered descending")
    
    include_tags: list[str] = Field(default_factory=list)
    exclude_tags: list[str] = Field(default_factory=list)
    
    created_after:Union[float,None] = Field(default=None)
    created_before:Union[float,None] = Field(default=None)
    
    md5:Union[str,None] = Field(default=None, regex=validate.MD5_REGEX)
    sha256:Union[str,None] = Field(default=None, regex=validate.SHA256_REGEX)


class Post(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At
    uploader: int = fields.Item_ID
    deleted: bool = Field(default=False, description="Whether the post has been deleted")
    source: str = Field(default="", description="The original source for the post")

    full: GenericMedia = Field(..., description="The full scale media for the Post")
    preview: Union[GenericMedia, None] = Field(default=None,description="A Medium Scale Version for the image, for hi-res posts")
    thumbnail: Image = Field(..., description="The lowest scale version of the image, for thumbnails")
    
    md5s: list[str] = Field(default_factory=list, description="The Post's MD5 hashes")
    sha256s: list[str] = Field(default_factory=list, description="The Post's SHA256 hashes")
    media_type: str = fields.Post_Type
    
    tags: list[str] = fields.Tags
    comments: list[int] = fields.Comments
    edits: list[PostEdit] = Field(default_factory=list, description="The edits made to the post")

    upvotes: int = Field(default=0, description="Number of upvotes on the Post")
    downvotes: int = Field(default=0, description="Number of downvotes on the Post")
