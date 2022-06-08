from typing import Union as _Union

from .types import GenericFile,BaseMedia,Dimensions,AnimationFile,ImageFile,VideoFile
from .image import Image
from .animation import Animation,isAnimatedSequence
from .video import Video

GenericMedia = _Union[Image,Video,Animation]

from .utils import predict_media_type
