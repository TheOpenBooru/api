from time import time
from pydantic import BaseModel, Field,AnyHttpUrl,FileUrl
from typing import Optional

from . import Image,Video,Animation

LanugageField = Field(default_factory=None, description="ISO 639-2 language code",regex="^[a-z]{3}$")
AgeRatingField = Field(default_factory=None, description="Age rating of the post", regex="^(safe|questionable|explicit)$")
SourceField = Field(default_factory=None, description="Source of the image")
TagsField = Field(default_factory=list, description="Tags on the post")


class Post_Edit(BaseModel):
    removed_tags: list[str] = TagsField
    added_tags: list[str] = TagsField
    from_language: Optional[str] = LanugageField
    to_language: str = LanugageField
    from_age_rating: Optional[str] = LanugageField
    to_age_rating: str = LanugageField
    from_source:Optional[AnyHttpUrl] = SourceField
    to_source:Optional[AnyHttpUrl] = SourceField

class Post(BaseModel):
    id: int = Field(..., description="The Post's ID")
    created_at: float = Field(default_factory=time, description="The Unix timestamp for when the Post was created")
    uploader: int = Field(..., description="The User ID of the Post Creator")

    full: Image|Video|Animation = Field(..., description="The full scale media for the Post")
    preview: Optional[Image|Video] = Field(..., description="A Medium Scale Version for the image, for hi-res posts")
    thumbnail: Image = Field(..., description="The lowest scale version of the image, for thumbnails")
    md5s: list[str] = Field(default_factory=list, description="The Post's MD5 hashes")
    sha256s: list[str] = Field(default_factory=list, description="The Post's SHA3-256 hashes")
    type: str = Field(..., description="Format of the post",regex="^(image|gif|video)$")
    
    tags: list[str] = TagsField
    language: Optional[str]   = LanugageField
    age_rating: Optional[str] = AgeRatingField
    source: Optional[AnyHttpUrl] = SourceField

    edit_history: list[Post_Edit] = Field(default_factory=list, description="Version Control History of the Post")
    comments: list[int] = Field(default_factory=list, description="Comments on the post")

    views: int = Field(default_factory=int, description="Number of views on the Post")
    upvotes: int = Field(default_factory=int, description="Number of upvotes on the Post")
    downvotes: int = Field(default_factory=int, description="Number of downvotes on the Post")
