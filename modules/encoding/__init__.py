from typing import Union as _Union

ACCEPTED_FILE_EXTENTIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".jpef",
    ".webp",
    ".apng",
    ".gif",
    ".webm",
    ".mp4",
}

from .probe import isAnimatedSequence, VideoProbe
from .types import GenericFile,BaseMedia,Dimensions,AnimationFile,ImageFile,VideoFile
from .image import Image
from .animation import Animation
from .video import Video

GenericMedia = _Union[Image,Video,Animation]

from .utils import generate_media
