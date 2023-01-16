from dataclasses import dataclass


@dataclass(frozen=True)
class ImageFile:
    data: bytes
    mimetype: str
    height: int
    width: int


@dataclass(frozen=True)
class AnimationFile:
    data: bytes
    mimetype: str
    height: int
    width: int
    frame_count: int
    duration: float


@dataclass(frozen=True)
class VideoFile:
    data: bytes
    mimetype: str
    height: int
    width: int
    duration: float
    framerate: str
    hasAudio: bool


GenericFile = ImageFile | AnimationFile | VideoFile
