from pydantic import BaseModel, Field
from . import fields

class BaseMedia(BaseModel):
    url: str = Field(..., description="The URI for the File")
    mimetype: str = fields.Mimetype
    height: int = Field(..., description="The Media's Height in pixels")
    width: int = Field(..., description="The Media's Width in pixels")

class Image(BaseMedia):
    type = "image"


class Animation(BaseMedia):
    type = "animation"
    duration: float = Field(..., description="The Video's Duration in framerate")
    frame_count: int = Field(..., description="The Video's Number of frames")
    duration:float = Field(..., description="The Video's Duration")

class Video(BaseMedia):
    type = "video"
    has_sound: bool = Field(..., description="Does the video contain sound?")
    duration: float = Field(..., description="The Video's Duration in framerate")
    fps: str = Field(..., description="The Video's Framerate in frames per second")

GenericMedia = Image | Animation | Video