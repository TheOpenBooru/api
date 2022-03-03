from dataclasses import dataclass
from typing_extensions import Self


class FileBase:
    data:bytes
    mimetype:str

@dataclass(frozen=True)
class Dimensions:
    width:int
    height:int


@dataclass(frozen=True)
class ImageFile(FileBase):
    data:bytes
    mimetype:str
    height:int
    width:int


@dataclass(frozen=True)
class AnimationFile(FileBase):
    data:bytes
    mimetype:str
    height:int
    width:int
    frame_count:int
    duration:float

@dataclass(frozen=True)
class VideoFile(FileBase):
    data:bytes
    mimetype:str
    height:int
    width:int
    duration:float
    framerate:float
    frame_count:int
    hasAudio:bool

class MediaBase:
    @classmethod
    async def from_bytes(cls,data:bytes) -> Self:
        ...

    async def full(self) -> ImageFile | AnimationFile | VideoFile:
        ...

    async def preview(self) -> ImageFile | VideoFile | None:
        ...

    async def thumbnail(self) -> ImageFile:
        ...
