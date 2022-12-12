from . import fields, BaseModel, Media, Image, MediaType, MAX_NUMBER
from modules import settings,validate
from pydantic import Field
from typing import Union, Optional
from enum import Enum


class Sort(str, Enum):
    id = "id"
    created_at = "created_at"
    upvotes = "upvotes"
    downvotes = "downvotes"


class Rating(str, Enum):
    unrated = "unrated"
    safe = "safe"
    sensitive = "sensitive"
    mature = "mature"
    explicit = "explicit"


class PostEdit(BaseModel):
    created_at: float = fields.created_at
    post_id: int = Field(..., description="The ID of the post the edit was performed on")
    editter_id: Union[int,None] = Field(default=None, description="The ID of the user who submitted this edit, None for system edits")
    
    tags: list[str] = Field(description="The tags for the post", regex=validate.TAG_REGEX, unique_items=True)
    sources: list[str] = Field(description="The sources for the post", regex=validate.URL_REGEX, unique_items=True)
    rating: Rating = Field(description="The rating for the post")


class PostQuery(BaseModel):
    index: int = Field(default=0, ge=0, lt=MAX_NUMBER, description="Offset from the start of the results")
    limit: int = Field(default=settings.POSTS_SEARCH_MAX_LIMIT, ge=0, lt=MAX_NUMBER, description="Maximum number of results to return")
    sort: Sort = Field(default=settings.POSTS_SEARCH_DEFAULT_SORT, description="How to sort the posts")
    descending: bool = Field(default=True, description="Should search be ordered descending")
    
    include_tags: list[str] = Field(default=[])
    exclude_tags: list[str] = Field(default=[])
    
    upvotes_gt: int = Field(default=0, ge=0, lt=MAX_NUMBER, description="Score should be greater than")
    upvotes_lt: int = Field(default=0, ge=0, lt=MAX_NUMBER, description="Score should be less than")
    
    created_after:Optional[float] = Field(default=None)
    created_before:Optional[float] = Field(default=None)
    
    creators:Optional[list[int]] = Field(default=None, ge=0, lt=MAX_NUMBER)
    ids:Optional[list[int]] = Field(default=None, ge=0, lt=MAX_NUMBER)
    md5:Optional[str] = Field(default=None, regex=validate.MD5_REGEX)
    sha256:Optional[str] = Field(default=None, regex=validate.SHA256_REGEX)
    source:Optional[str] = Field(default=None, regex=validate.URL_REGEX)
    
    media_types:Optional[list[MediaType]] = Field(default=None, regex=validate.URL_REGEX)
    ratings: Optional[list[Rating]] = Field(default=[], description="Ratings to exlucde from the results")


class Hashes(BaseModel):
    md5s: list[bytes] = Field(default_factory=list, description="A list of MD5 Hashes")
    sha256s: list[bytes] = Field(default_factory=list, description="A list of SHA2 256bit Hashes")
    phashes: list[bytes] = Field(default_factory=list, description="A list of SHA2 256bit Hashes")


class Post(BaseModel):
    id: int = Field(..., lt=2**64, description="The Post's Unique Id")
    created_at: float = fields.created_at
    uploader: Union[int, None] = Field(default=None, description="The user ID of the person who uploaded this post, null means no creator")
    sources: list[str] = Field(default_factory=list, description="The original source for the post")
    rating: Rating = Field(default=Rating.unrated, description="The default rating for a post")

    full: Media = Field(..., description="The full scale media for the Post")
    preview: Union[Media, None] = Field(default=None,description="A Medium Scale Version for the image, for hi-res posts")
    media: list[Media] = Field(default_factory=list, description="All media related to this post")
    thumbnail: Image = Field(..., description="A low quality image used for thumbnails")

    hashes: Hashes = Field(default_factory=Hashes, description="A table of all the posts hashes")
    protected_tags: list[str] = fields.tags
    tags: list[str] = fields.tags
    edits: list[PostEdit] = Field(default_factory=list, description="The edits made to the post")

    upvotes: int = Field(default=0, description="Number of upvotes on the Post")
    downvotes: int = Field(default=0, description="Number of downvotes on the Post")
