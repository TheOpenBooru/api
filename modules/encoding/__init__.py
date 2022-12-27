from ._types import GenericFile, AnimationFile, ImageFile, VideoFile
from .probe import VideoProbe
from . import probe
from .encoder import BaseEncoder
from .image import ImageEncoder
from .animation import AnimationEncoder
from .video import VideoEncoder
from .utils import generate_encoder, encode_media

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
