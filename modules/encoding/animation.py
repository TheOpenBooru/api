from . import MediaBase,AnimationFile,ImageFile,Image
import io
from dataclasses import dataclass
from typing_extensions import Self
from PIL import Image as PILImage

@dataclass
class Animation(MediaBase):
    _PIL:PILImage.Image
    _height:int
    _width:int
    _frame_count:int
    
    @classmethod
    async def from_bytes(cls,data:bytes) -> Self:
        """Raises:
        - ValueError: Could not Load Animation
        - ValueError: Has Only 1 Frame
        """
        buf = io.BytesIO(data)
        try:
            # formats=None means attempt to load all formats
            pil = PILImage.open(buf,formats=None)
        except Exception:
            raise ValueError("Could not Load Animation")
        
        if pil.n_frames == 1:
            raise ValueError("Has Only 1 Frame")

        return Animation(
            _PIL=pil,
            _height=pil.height,
            _width=pil.width,
            _frame_count=pil.n_frames,
        )

    async def full(self) -> AnimationFile:
        buf = io.BytesIO()
        frame_durations = self._get_animation_durations()
        self._PIL.save(
            buf,
            'webp',
            save_all=True, # save_all=True menas save as an animation
            duration=frame_durations,
            background=(0,0,0,0),
        )

        duration = sum(frame_durations) / 1000
        return AnimationFile(
            data=buf.getvalue(),
            mimetype='image/webp',
            height=self._height,
            width=self._width,
            frame_count=self._frame_count,
            duration=duration,
        )

    def _get_animation_durations(self):
        frame_durations = []
        for x in range(self._PIL.n_frames):
            self._PIL.seek(x)
            frame = self._PIL.copy()
            duration = frame.info['duration']
            frame_durations.append(int(duration))
        
        return frame_durations

    async def preview(self) -> None:
        return None
    
    async def thumbnail(self) -> ImageFile:
        img = Image.from_pillow(self._PIL)
        return await img.thumbnail()