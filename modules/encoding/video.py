from . import BaseMedia,ImageFile,VideoFile,Image
from .probe import VideoProbe
from modules import settings
import os
import shutil
import random
import ffmpeg
from pathlib import Path

class Video(BaseMedia):
    type = "video"
    _filepath: str
    _probe: VideoProbe
    
    def __init__(self,data:bytes):
        self._data = data


    def __enter__(self):
        self._rand_id = random.randint(0,2**32)
        self._filepath = f"/tmp/{self._rand_id}"
        with open(self._filepath,'wb') as f:
            f.write(self._data)
        self._probe = VideoProbe(self._filepath)
        new_path = self._filepath
        shutil.move(self._filepath,new_path)
        self._filepath = new_path
        return self


    def __exit__(self, type, value, tb):
        os.remove(self._filepath)


    def full(self) -> VideoFile:
        """Raises:
        - FileNotFoundError: Didn't use `with` statement to create file
        """
        probe = self._probe
        return VideoFile(
            self._data,probe.mimetype,
            probe.height,probe.width,
            probe.duration,probe.framerate,
            probe.audio
        )



    def preview(self) -> None:
        """Raises:
        - FileNotFoundError: Didn't use `with` statement to create file
        """
        return None



    def thumbnail(self) -> ImageFile:
        """Raises:
        - FileNotFoundError: Didn't use `with` statement to create file
        """
        offset_percentage = 0.01 * settings.VIDEO_THUMBNAIL_OFFSET
        try:
            data,err = (
                ffmpeg
                .input(self._filepath)
                .output("pipe:",
                    f='image2',vframes=1
                )
                .run(input=self._data,capture_stdout=True,capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise ValueError(e.stderr)
        else:
            with Image(data) as img:
                return img.thumbnail()