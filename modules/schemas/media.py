from pydantic import Field
from . import BaseModel

class BaseMedia(BaseModel):
    url: str = Field(..., description="The URI for the File")
    mimetype: str = Field(..., description="The Media's Mimetype")
    height: int = Field(..., description="The Media's Height in pixels")
    width: int = Field(..., description="The Media's Width in pixels")

class Image(BaseMedia):
    type: str = Field(default="image", description="The type of media")


class Animation(BaseMedia):
    duration: float = Field(..., description="The Animation's Duration in framerate")
    frame_count: int = Field(..., description="The Animation's Number of frames")
    duration:float = Field(..., description="The Animation's Duration")
    type:str = Field(default="animation", description="The type of media")

class Video(BaseMedia):
    has_sound: bool = Field(..., description="Does the video contain sound?")
    duration: float = Field(..., description="The Video's Duration in framerate")
    fps: str = Field(..., description="The Video's Framerate in frames per second")
    type = Field(default="video", description="The type of media")

GenericMedia = Image | Animation | Video