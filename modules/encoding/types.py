from modules import schemas
from dataclasses import dataclass
from functools import cache, cached_property
from typing import Union


@dataclass(frozen=True)
class Dimensions:
    width:int
    height:int


@dataclass(frozen=True)
class ImageFile:
    data:bytes
    mimetype:str
    height:int
    width:int


@dataclass(frozen=True)
class AnimationFile:
    data:bytes
    mimetype:str
    height:int
    width:int
    frame_count:int
    duration:float


@dataclass(frozen=True)
class VideoFile:
    data:bytes
    mimetype:str
    height:int
    width:int
    duration:float
    framerate:str
    hasAudio:bool

GenericFile = Union[ImageFile,AnimationFile,VideoFile]

class BaseMedia:
    type:schemas.MediaType
    def __init__(self,data:bytes):
        """Raises:
        - ValueError: Could not Parse Data
        """

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        pass

    @cache
    def full(self) -> GenericFile:
        """Raises:
        - FileNotFoundError: Didn't use with statement to create file
        """
        ...

    @cache
    def preview(self) -> Union[GenericFile,None]:
        """Raises:
        - FileNotFoundError: Didn't use with statement to create file
        """
        ...

    @cache
    def thumbnail(self) -> GenericFile:
        """Raises:
        - FileNotFoundError: Didn't use with statement to create file
        """
        ...
