from . import fields,BaseModel,GenericMedia,Image
from modules import settings,validate
from pydantic import Field
from typing import Union, Optional
from enum import Enum


class Valid_Post_Sorts(str, Enum):
    id = "id"
    created_at = "created_at"
    upvotes = "upvotes"
    downvotes = "downvotes"


class Valid_Post_Ratings(str, Enum):
    unrated = "unrated"
    safe = "safe"
    sensitive = "sensitive"
    mature = "mature"
    explicit = "explicit"



class Post_Edit(BaseModel):
    created_at: float = fields.Created_At
    post_id: int = Field(..., description="The ID of the post the edit was performed on")
    editter_id: Union[int,None] = Field(default=None, description="The ID of the user who submitted this edit, None for system edits")
    
    old_tags: list[str] = Field(default=None, description="The Tags added in this edit")
    new_tags: list[str] = Field(default=None, description="The Tags added in this edit")
    
    old_source: str = Field(default="", description="The previous source for the post")
    new_source: str = Field(default="", description="The new source for the post")
    
    old_rating: str = Field(default="", description="The previous source for the post")
    new_rating: str = Field(default="", description="The new source for the post")


class Post_Query(BaseModel):
    index: int = Field(default=0, description="Offset from the start of the results")
    limit: int = Field(default=64, description="Maximum number of results to return")
    sort: Valid_Post_Sorts = Field(default=settings.POSTS_SEARCH_DEFAULT_SORT, description="How to sort the posts")
    exclude_ratings: list[Valid_Post_Ratings] = Field(default_factory=list, description="Ratings to exlucde from the results")
    descending: bool = Field(default=True, description="Should search be ordered descending")
    
    include_tags: list[str] = Field(default_factory=list)
    exclude_tags: list[str] = Field(default_factory=list)
    
    created_after:Union[float,None] = Field(default=None)
    created_before:Union[float,None] = Field(default=None)
    
    md5:Union[str,None] = Field(default=None, regex=validate.MD5_REGEX)
    sha256:Union[str,None] = Field(default=None, regex=validate.SHA256_REGEX)


class Hashes(BaseModel):
    md5s: list[str] = Field(default_factory=list, description="A list of MD5 Hashes")
    sha256s: list[str] = Field(default_factory=list, description="A list of SHA2 256bit Hashes")
    phash: list[str] = Field(default_factory=list, description="A list of SHA2 256bit Hashes")


class Post(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At
    uploader: int = fields.Item_ID
    deleted: bool = Field(default=False, description="Whether the post has been deleted")
    source: str = Field(default="", description="The original source for the post")
    rating: Valid_Post_Ratings = Field(default="unrated", description="The default rating for a post")

    full: GenericMedia = Field(..., description="The full scale media for the Post")
    preview: Union[GenericMedia, None] = Field(default=None,description="A Medium Scale Version for the image, for hi-res posts")
    # qualities: list[GenericMedia] = Field(default_factory=list, description="List of all qualities of this post")
    thumbnail: Image = Field(..., description="A low quality image used for thumbnails")

    media_type: str = fields.Post_Type
    hashes: Hashes = Field(default_factory=Hashes, description="A table of all the posts hashes")

    tags: list[str] = fields.Tags
    comments: list[int] = fields.Comments
    edits: list[Post_Edit] = Field(default_factory=list, description="The edits made to the post")

    upvotes: int = Field(default=0, description="Number of upvotes on the Post")
    downvotes: int = Field(default=0, description="Number of downvotes on the Post")
