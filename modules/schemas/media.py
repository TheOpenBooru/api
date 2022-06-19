from typing import Union
from . import BaseModel
from pydantic import Field
from enum import Enum

class Type(str, Enum):
    image = 'image'
    video = 'video'
    animation = 'animation'

class BaseMedia(BaseModel):
    url: str = Field(..., description="The URI for the File")
    mimetype: str = Field(..., description="The Media's Mimetype")
    height: int = Field(..., description="The Media's Height in pixels")
    width: int = Field(..., description="The Media's Width in pixels")
    type: Type

class Image(BaseMedia):
    type: Type = Field(default="image", description="The type of media")


class Animation(BaseMedia):
    duration: float = Field(..., description="The Animation's Duration in framerate")
    frame_count: int = Field(..., description="The Animation's Number of frames")
    duration:float = Field(..., description="The Animation's Duration")
    type:Type = Field(default="animation", description="The type of media")

class Video(BaseMedia):
    has_sound: bool = Field(..., description="Does the video contain sound?")
    duration: float = Field(..., description="The Video's Duration in framerate")
    fps: str = Field(..., description="The Video's Framerate in frames per second")
    type:Type = Field(default="video", description="The type of media")

GenericMedia = Union[Image,Animation,Video]