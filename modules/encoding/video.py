from . import BaseEncoder, ImageFile, VideoFile, ImageEncoder
from .probe import VideoProbe
from modules import settings, schemas
import os
import shutil
import random
import ffmpeg
from typing import Union


class VideoEncoder(BaseEncoder):
    type = schemas.MediaType.video
    filepath: Union[str, None] = None
    probe: VideoProbe

    def __init__(self, data: bytes):
        self._data = data

    def __enter__(self):
        rand_id = random.randint(0, 2**32)
        path = self.filepath = f"/tmp/{rand_id}"

        with open(path, 'wb') as f:
            f.write(self._data)
        self.probe = VideoProbe(path)

        return self

    def __exit__(self, *args):
        if self.filepath:
            os.remove(self.filepath)

    def original(self) -> VideoFile:
        """Raises:
        - FileNotFoundError: Didn't use `with` statement to create file
        """
        if self.filepath == None:
            raise FileNotFoundError(
                "Didn't use `with` statement to create file")

        probe = self.probe
        return VideoFile(
            self._data,
            mimetype=probe.mimetype,
            height=probe.height,
            width=probe.width,
            duration=probe.duration,
            framerate=probe.framerate,
            hasAudio=probe.audio,
        )

    def preview(self) -> None:
        """Raises:
        - FileNotFoundError: Didn't use `with` statement to create file
        """
        if self.filepath == None:
            raise FileNotFoundError(
                "Didn't use `with` statement to create file")

        return None

    def thumbnail(self) -> ImageFile:
        """Raises:
        - FileNotFoundError: Didn't use `with` statement to create file
        """
        if self.filepath == None:
            raise FileNotFoundError(
                "Didn't use `with` statement to create file")

        offset_percentage = 0.01 * settings.VIDEO_THUMBNAIL_OFFSET
        offset_time = float(offset_percentage * self.probe.duration)
        thumbnail_offset = min(self.probe.duration, offset_time)

        try:
            data, err = (
                ffmpeg
                .input(self.filepath)
                .output(
                    "pipe:",
                    f='image2',
                    vframes=1,
                    ss=thumbnail_offset,
                )
                .run(
                    input=self._data,
                    capture_stdout=True,
                    capture_stderr=True
                )
            )
        except ffmpeg.Error as e:
            raise ValueError(e.stderr)
        else:
            with ImageEncoder(data) as img:
                return img.thumbnail()
