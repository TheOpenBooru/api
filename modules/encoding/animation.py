from . import BaseEncoder, AnimationFile, ImageFile, ImageEncoder
from modules import schemas
import io
import warnings
from typing_extensions import Self
from PIL import Image as PILImage

warnings.simplefilter('ignore', PILImage.DecompressionBombWarning)
PILImage.MAX_IMAGE_PIXELS = (5000 * 5000) * 2
# x2 max pixels, warning is raised on MAX_IMAGE_PIXELS


class AnimationEncoder(BaseEncoder):
    type = schemas.MediaType.animation
    _pillow: PILImage.Image
    _data: bytes
    _height: int
    _width: int
    _frame_count: int
    _duration: float

    def __init__(self, data: bytes):
        """Raises:
        - ValueError: Could not Load Animation
        - ValueError: Animation was too large
        - ValueError: Has Only 1 Frame
        """
        buf = io.BytesIO(data)

        try:
            pillow = PILImage.open(buf, formats=None)
            # formats=None attempt to load all formats
        except PILImage.DecompressionBombError:
            raise ValueError("Animation was too large")
        except Exception:
            raise ValueError("Could not Load Animation")
        if pillow.n_frames == 1:
            raise ValueError("Animation Only Has 1 Frame")

        frame_durations = get_frame_durations(pillow)
        duration = sum(frame_durations) / 1000

        self._data = data
        self._pillow = pillow
        self._height = pillow.height
        self._width = pillow.width
        self._frame_count = pillow.n_frames
        self._duration = duration

    def original(self) -> AnimationFile:
        data = encode_pillow_animation(self._pillow)
        return AnimationFile(
            data=data,
            mimetype='image/webp',
            height=self._height,
            width=self._width,
            frame_count=self._frame_count,
            duration=self._duration,
        )

    def preview(self) -> ImageFile:
        buf = io.BytesIO()
        self._pillow.seek(0)
        self._pillow.save(
            buf,
            format='webp',
            quality=100,
            lossless=True
        )
        return ImageFile(
            data=buf.read(),
            mimetype="image/webp",
            height=self._pillow.height,
            width=self._pillow.width,
        )

    def thumbnail(self) -> ImageFile:
        with ImageEncoder(self._data) as img:
            return img.thumbnail()


def encode_pillow_animation(pillow: PILImage.Image) -> bytes:
    buf = io.BytesIO()
    frame_durations = get_frame_durations(pillow)
    pillow.save(
        buf,
        'WEBP',
        save_all=True,  # Save as an animation
        transparency=0,
        duration=frame_durations,
        background=(0, 0, 0, 0),  # RGBA,
        disposal=2,
    )
    return buf.getvalue()


def get_frame_durations(pillow: PILImage.Image) -> list[int]:
    frame_durations = []
    for x in range(pillow.n_frames):
        pillow.seek(x)
        duration = int(pillow.info['duration'])
        frame_durations.append(duration)
    
    return frame_durations