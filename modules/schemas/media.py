from . import BaseModel
from modules import store
from typing import Union
from pydantic import Field
from enum import Enum


class MediaType(str, Enum):
    image = "image"
    animation = "animation"
    video = "video"


class BaseMedia(BaseModel):
    url: str = Field(...,  description="The URI for the File")
    mimetype: str = Field(..., description="The Media's Mimetype")
    height: int = Field(..., description="The Media's Height in pixels")
    width: int = Field(..., description="The Media's Width in pixels")
    type: MediaType

    def __init__(self, *, url: str, **kwargs):
        kwargs["url"] = store.to_absolute_url(url)
        return super().__init__(**kwargs)

class Image(BaseMedia):
    type: MediaType = MediaType.image


class Animation(BaseMedia):
    frame_count: int | None = Field(
        default=None, description="The Animation's Number of frames")
    duration: float | None = Field(
        default=None, description="The Animation's Duration")
    type: MediaType = MediaType.animation


class Video(BaseMedia):
    has_sound: bool | None = Field(
        default=None, description="Does the video contain sound?")
    duration: float | None = Field(
        default=None, description="The Video's Duration in framerate")
    fps: str | None = Field(
        default=None, description="The Video's Framerate in frames per second")
    type: MediaType = MediaType.video


Media = Union[Image, Animation, Video]