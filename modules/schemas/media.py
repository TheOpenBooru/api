from typing import Union
from . import BaseModel
from pydantic import Field
from enum import Enum

class MediaType(str, Enum):
    image = "image"
    animation = "animation"
    video = "video"


class BaseMedia(BaseModel):
    url: str = Field(..., description="The URI for the File")
    mimetype: str = Field(..., description="The Media's Mimetype")
    height: int = Field(..., description="The Media's Height in pixels")
    width: int = Field(..., description="The Media's Width in pixels")
    type: MediaType


class Image(BaseMedia):
    type: MediaType = Field(default=MediaType.image, description="The type of media")


class Animation(BaseMedia):
    duration: float = Field(..., description="The Animation's Duration in framerate")
    frame_count: int = Field(..., description="The Animation's Number of frames")
    duration:float = Field(..., description="The Animation's Duration")
    type:MediaType = Field(default=MediaType.animation, description="The type of media")

class Video(BaseMedia):
    has_sound: bool = Field(..., description="Does the video contain sound?")
    duration: float = Field(..., description="The Video's Duration in framerate")
    fps: str = Field(..., description="The Video's Framerate in frames per second")
    type:MediaType = Field(default=MediaType.video, description="The type of media")

GenericMedia = Union[Image,Animation,Video]