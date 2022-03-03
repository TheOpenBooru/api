from pydantic import BaseModel, Field,FileUrl

class MediaBase(BaseModel):
    url: str = Field(..., description="The URI for the File")
    mimetype: str = Field(..., description="The MIME type for the File",regex="^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$")

class Image(MediaBase):
    height: int = Field(..., description="The Image's Height in pixels")
    width: int = Field(..., description="The Image's Width in pixels")


class Animation(MediaBase):
    height: int = Field(..., description="The Videos's Height in pixels")
    width: int = Field(..., description="The Video's Width in pixels")
    duration: float = Field(..., description="The Video's Duration in framerate")
    frame_count: int = Field(..., description="The Video's Number of frames")
    duration:float = Field(..., description="The Video's Duration")

class Video(MediaBase):
    has_sound: bool = Field(..., description="Does the video contain sound?")
    height: int = Field(..., description="The Videos's Height in pixels")
    width: int = Field(..., description="The Video's Width in pixels")
    duration: float = Field(..., description="The Video's Duration in framerate")
    frame_count: int = Field(..., description="The Video's Number of frames")
    fps: float = Field(..., description="The Video's Framerate in frames per second")
