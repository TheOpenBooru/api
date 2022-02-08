import pydantic
from pydantic import BaseModel, Field,AnyHttpUrl,FileUrl
from typing import Any, Optional


class Image(BaseModel):
    uri: FileUrl = Field(..., description="The Image's URI")
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
    user_id: int = Field(..., description="The ID of the Account Bound to the Author")


class Source(BaseModel):
    author: Author = Field(..., description="The Author of the source")
    created_at: str = Field(..., description="The Unix Timestamp for when the source was created")
    url: pydantic.AnyHttpUrl = Field(..., description="Source of the image")


class Tag(BaseModel):
    name: str = Field(...,description="The Tag Name")
    namespace: str = Field(..., description="The Tag Namespace")
    created_at: int = Field(..., description="The Unix Timestamp for the First Usage of the tag")
    count: Optional[int] = Field(None, description="The number of times the tag has been used")


class User(BaseModel):
    id: int = Field(..., description="The User's ID")
    created_at: int = Field(..., description="Unix timestamp for when the User was created")
    name: str = Field(..., description="The User's Name")
    level: str = Field(..., description="The User's Level")
    bio: str = Field("", description="The User's Biography for their profile")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")

    email: Optional[str] = Field(None, description="The User's Email Address")
    settings: Optional[str] = Field(None, description="The User's Email Address")
    history: Optional[list[int]] = Field(None, description="IDs of recently viewed posts")
    favourites: Optional[list[int]] = Field(None, description="IDs of posts the user has favourited")
    blocked: Optional[list[int]] = Field(None, description="IDs of posts the user has blocked")


class Post(BaseModel):
    id: int = Field(..., description="The Post's ID")
    sha3_256: list[str] = Field(..., description="The Post's SHA3-256 hashes")
    md5s: list[str] = Field(..., description="The Post's MD5 hashes")
    creator: int = Field(..., description="The Post creator's user ID")
    created_at: int = Field(..., description="The Unix timestamp for when the Post was created")

    type: str = Field(..., description="Format of the post",regex="image|gif|video")
    sound: bool = Field(..., description="Does the post contain sound?")
    language: Optional[str] = Field(None, description="ISO 639-2 language code",min_length=3, max_length=3)
    source: Optional[str] = Field(None, description="Original Source of the Post")
    rating: Optional[str] = Field(None, description="Age rating of the post", regex="safe|questionable|explicit")

    tags: list[str] = Field(default_factory=list, description="Tags on the post")
    comments: list[int] = Field(default_factory=list, description="Comments on the post")

    views: int = Field(0, description="Number of views on the Post")
    upvotes: int = Field(0, description="Number of upvotes on the Post")
    downvotes: int = Field(0, description="Number of downvotes on the Post")

    full: Image = Field(..., description="The largest scale image for the Post")
    preview: Optional[Image] = Field(None, description="Medium-Scale Version for the image, for hi-res posts")
    thumbnail: Image = Field(..., description="The lowest scale version of the image, for thumbnails")


class Comment(BaseModel):
    id: int = Field(..., description="The Comment's ID")
    created_at: int = Field(..., description="The Unix timestamp for when the Comment was created")
    creator: int = Field(..., description="The User ID of the Comment Creator")
    text: str = Field(..., description="The Comment's text")
    post: int = Field(..., description="The Post ID the Comment is on")
