from . import fields,BaseModel,GenericMedia,Image
from modules import settings,validate
from pydantic import Field
from typing import Union, Optional
from enum import Enum


class Sort(str, Enum):
    id = "id"
    created_at = "created_at"
    upvotes = "upvotes"
    downvotes = "downvotes"


class MediaType(str, Enum):
    image = "image"
    animation = "animation"
    video = "video"

class Rating(str, Enum):
    unrated = "unrated"
    safe = "safe"
    sensitive = "sensitive"
    mature = "mature"
    explicit = "explicit"



class Post_Edit(BaseModel):
    created_at: float = fields.Created_At
    post_id: int = Field(..., description="The ID of the post the edit was performed on")
    editter_id: Union[int,None] = Field(default=None, description="The ID of the user who submitted this edit, None for system edits")
    
    old_tags: list[str] = Field(default=None, description="The tags for the post before edit", regex=validate.TAG_REGEX, unique_items=True)
    new_tags: list[str] = Field(default=None, description="The Tags added in this edit", regex=validate.TAG_REGEX, unique_items=True)
    
    old_source: str = Field(default="", description="The source for the post before edit")
    new_source: str = Field(default="", description="The new source for the post")
    
    old_rating: str = Field(default="", description="The rating for the post before edit")
    new_rating: str = Field(default="", description="The new rating for the post")


class Post_Query(BaseModel):
    index: int = Field(default=0, description="Offset from the start of the results")
    limit: int = Field(default=settings.POSTS_SEARCH_MAX_LIMIT, description="Maximum number of results to return")
    sort: Sort = Field(default=settings.POSTS_SEARCH_DEFAULT_SORT, description="How to sort the posts")
    descending: bool = Field(default=True, description="Should search be ordered descending")
    
    
    include_tags: list[str] = Field(default=[])
    exclude_tags: list[str] = Field(default=[])
    
    upvotes_gt:int = Field(default=0, description="Score should be greater than")
    upvotes_lt:int = Field(default=0, description="Score should be less than")
    
    created_after:Optional[float] = Field(default=None)
    created_before:Optional[float] = Field(default=None)
    
    ids:Optional[list[int]] = Field(default=None)
    md5:Optional[str] = Field(default=None, regex=validate.MD5_REGEX)
    sha256:Optional[str] = Field(default=None, regex=validate.SHA256_REGEX)
    source:Optional[str] = Field(default=None, regex=validate.URL_REGEX)
    media_types:Optional[list[MediaType]] = Field(default=None, regex=validate.URL_REGEX)
    ratings: Optional[list[Rating]] = Field(default=[], description="Ratings to exlucde from the results")


class Hashes(BaseModel):
    md5s: list[str] = Field(default_factory=list, description="A list of MD5 Hashes")
    sha256s: list[str] = Field(default_factory=list, description="A list of SHA2 256bit Hashes")
    phash: list[str] = Field(default_factory=list, description="A list of SHA2 256bit Hashes")


class Post(BaseModel):
    id: int = Field(...,description="The Post's Unique Id")
    created_at: float = fields.Created_At
    uploader: Union[int, None] = Field(default=None, description="The user ID of the person who uploaded this post, null means no creator")
    deleted: bool = Field(default=False, description="Whether the post has been deleted")
    source: str = Field(default="", description="The original source for the post")
    rating: Rating = Field(default="unrated", description="The default rating for a post")

    full: GenericMedia = Field(..., description="The full scale media for the Post")
    preview: Union[GenericMedia, None] = Field(default=None,description="A Medium Scale Version for the image, for hi-res posts")
    thumbnail: Image = Field(..., description="A low quality image used for thumbnails")

    media_type: MediaType = Field( ..., description="Format of the post", regex="^(image|animation|video)$",)
    hashes: Hashes = Field(default_factory=Hashes, description="A table of all the posts hashes")

    tags: list[str] = fields.Tags
    comments: list[int] = fields.Comments
    edits: list[Post_Edit] = Field(default_factory=list, description="The edits made to the post")

    upvotes: int = Field(default=0, description="Number of upvotes on the Post")
    downvotes: int = Field(default=0, description="Number of downvotes on the Post")
