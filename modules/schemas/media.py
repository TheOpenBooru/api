from pydantic import BaseModel, Field,FileUrl

MimetypeField = Field(..., description="The Image's MIME type",regex="^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$")

class Image(BaseModel):
    url: str = Field(..., description="The Image's URI")
    mimetype: str = MimetypeField
    
    height: int = Field(..., description="The Image's Height in pixels")
    width: int = Field(..., description="The Image's Width in pixels")


class Video(BaseModel):
    uri: FileUrl = Field(..., description="The Video's URI")
    mimetype: str = MimetypeField
    has_sound: bool = Field(..., description="Does the video contain sound?")
    
    height: int = Field(..., description="The Videos's Height in pixels")
    width: int = Field(..., description="The Video's Width in pixels")
    duration: int = Field(..., description="The Video's Duration in framerate")
    frames: int = Field(..., description="The Video's Number of frames")
    fps: float = Field(..., description="The Video's Framerate in frames per second")
