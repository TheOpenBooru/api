import asyncio
from . import BaseMedia,AnimationFile,ImageFile,Image
import io
from dataclasses import dataclass
from typing_extensions import Self
from PIL import Image as PILImage

@dataclass
class Animation(BaseMedia):
    type="gif"
    _PIL:PILImage.Image
    _height:int
    _width:int
    _frame_count:int
    _duration:float
    
    @classmethod
    async def from_bytes(cls,data:bytes) -> Self:
        """Raises:
        - ValueError: Could not Load Animation
        - ValueError: Animation was too large
        - ValueError: Has Only 1 Frame
        """
        PILImage.MAX_IMAGE_PIXELS = (5000*5000)*2
        # x2 becasue actual max pixels is half
        buf = io.BytesIO(data)
        try:
            # formats=None:attempt to load all formats
            pillow = PILImage.open(buf,formats=None)
        except PILImage.DecompressionBombError:
            raise ValueError("Animation was too large")
        except Exception:
            raise ValueError("Could not Load Animation")
        if pillow.n_frames == 1:
            raise ValueError("Has Only 1 Frame")
        
        frame_durations = _pillow_animation_durations(pillow)
        duration = sum(frame_durations) / 1000

        return Animation(
            _PIL=pillow,
            _height=pillow.height,
            _width=pillow.width,
            _frame_count=pillow.n_frames,
            _duration=duration,
        )

    async def full(self) -> AnimationFile:
        data = await _pillow_animation_to_bytes(self._PIL)
        return AnimationFile(
            data=data,
            mimetype='image/gif',
            height=self._height,
            width=self._width,
            frame_count=self._frame_count,
            duration=self._duration,
        )


    async def preview(self) -> None:
        return None


    async def thumbnail(self) -> ImageFile:
        img = Image.from_pillow(self._PIL)
        return await img.thumbnail()


async def _pillow_animation_to_bytes(pillow:PILImage.Image) -> bytes:
    buf = io.BytesIO()
    frame_durations = _pillow_animation_durations(pillow)
    pillow.save(
        buf,
        'WEBP',
        save_all=True, #  save as an animation
        transparency=0,
        duration=frame_durations[0],
        background=[0]*4,
    )
    return buf.getvalue()


def _pillow_animation_durations(pillow:PILImage.Image) -> list:
    frame_durations = []
    for x in range(pillow.n_frames):
        pillow.seek(x)
        duration = int(pillow.info['duration'])
        frame_durations.append(duration)
    return frame_durations
