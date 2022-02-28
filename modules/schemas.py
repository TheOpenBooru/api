import pydantic
import time
from pydantic import BaseModel, Field,AnyHttpUrl,FileUrl
from typing import Any, Optional


class Image(BaseModel):
    url: str = Field(..., description="The Image's URI")
    height: int = Field(..., description="The Image's Height in pixels")
    width: int = Field(..., description="The Image's Width in pixels")
    mimetype: str = Field(..., description="The Image's MIME type")


class Video(BaseModel):
    uri: FileUrl = Field(..., description="The Video's URI")
    height: int = Field(..., description="The Videos's Height in pixels")
    width: int = Field(..., description="The Video's Width in pixels")
    duration: int = Field(..., description="The Video's Duration in framerate")
    frames: int = Field(..., description="The Video's Number of frames")
    fps: float = Field(..., description="The Video's Framerate in frames per second")
    mimetype: str = Field(..., description="The Video's MIME type")


class Author(BaseModel):
    name: str = Field(..., description="The Author's Name")
    avatar: Image = Field(..., description="The Author's Avatar")
    aliases: list[str] = Field(default_factory=list, description="Other Names for the Author")
    user_account: int = Field(..., description="The ID of the Account Bound to the Author")


class Tag(BaseModel):
    created_at: float = Field(default_factory=time.time, description="The Unix Timestamp for the First Usage of the tag")
    name: str = Field(...,description="The Tag Name")
    namespace: str = Field(..., description="The Tag Namespace")
    count: int = Field(default_factory=int, description="The number of times the tag has been used")


class Comment(BaseModel):
    id: int = Field(..., description="The Comment's ID")
    created_at: float = Field(default_factory=time.time, description="The Unix timestamp for when the Comment was created")
    creator: int = Field(..., description="The User ID of the Comment Creator")
    text: str = Field(..., description="The Comment's text")
    post: int = Field(..., description="The Post ID the Comment is on")


class User_Public(BaseModel):
    id: int = Field(..., description="The User's ID")
    created_at: float = Field(default_factory=time.time, description="Unix timestamp for when the User was created")

    name: str = Field(..., description="The User's Name")
    level: str = Field(default_factory=lambda:"USER", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")

class User(User_Public):
    email: str = Field(..., description="The User's Email Address")
    settings: str = Field(default_factory=str, description="The User's Settings")
    
    upvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has upvoted")
    downvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has downvoted")
    history: list[int] = Field(default_factory=list, description="IDs of recently viewed posts")

class Post(BaseModel):
    id: int = Field(..., description="The Post's ID")
    created_at: float = Field(default_factory=time.time, description="The Unix timestamp for when the Post was created")
    uploader: int = Field(..., description="The User ID of the Post Creator")
    md5s: list[str] = Field(default_factory=list, description="The Post's MD5 hashes")
    sha256s: list[str] = Field(default_factory=list, description="The Post's SHA3-256 hashes")
    type: str = Field(..., description="Format of the post",regex="^(image|gif|video)$")
    
    work_author: Optional[Author] = Field(default_factory=None, description="The Author of the source")
    source: Optional[pydantic.AnyHttpUrl] = Field(default_factory=None, description="Source of the image")
    sound: bool = Field(default_factory=bool, description="Does the post contain sound?")
    language: Optional[str]   = Field(default_factory=None, description="ISO 639-2 language code",regex="^[a-z]{3}$")
    age_rating: Optional[str] = Field(default_factory=None, description="Age rating of the post", regex="^(safe|questionable|explicit)$")

    edit_history: list[None] = Field(default_factory=list, description="Version Control History of the Post")
    tags: list[str] = Field(default_factory=list, description="Tags on the post")
    comments: list[int] = Field(default_factory=list, description="Comments on the post")

    views: int = Field(default_factory=int, description="Number of views on the Post")
    upvotes: int = Field(default_factory=int, description="Number of upvotes on the Post")
    downvotes: int = Field(default_factory=int, description="Number of downvotes on the Post")

    full: Image =     Field(..., description="The largest scale image for the Post")
    preview: Image = Field(..., description="Medium-Scale Version for the image, for hi-res posts")
    thumbnail: Image = Field(..., description="The lowest scale version of the image, for thumbnails")
