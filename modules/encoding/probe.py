from functools import cached_property
import mimetypes
from typing import Union
from magic import Magic
from PIL import Image as PILImage
import ffmpeg
import io


class VideoProbe:
    filepath: str
    data: bytes

    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            self.data = f.read()
        self.filepath = filepath
        self.probe_data = ffmpeg.probe(self.filepath)

    @cached_property
    def video_stream(self) -> dict:
        streams = self.probe_data['streams']
        video_streams = [x for x in streams if x['codec_type'] == 'video']
        if len(video_streams) == 1:
            return video_streams[0]
        else:
            raise Exception('No or Multiple Video Streams Found')

    @cached_property
    def height(self) -> int:
        return int(self.video_stream['height'])

    @cached_property
    def width(self) -> int:
        return int(self.video_stream['width'])

    @cached_property
    def framerate(self) -> str:
        framerate = eval(self.video_stream['r_frame_rate'])
        if framerate % 1 == 0:
            framerate = int(framerate)

        return str(framerate)

    @cached_property
    def mimetype(self) -> str:
        magic = Magic(mime=True)
        return magic.from_buffer(self.data)

    @cached_property
    def extention(self) -> str:
        ext = mimetypes.guess_extension(self.mimetype)
        if ext == None:
            raise Exception("Couldn't Guess File Extention")
        return ext

    @cached_property
    def audio(self) -> bool:
        for stream in self.probe_data['streams']:
            if stream['codec_type'] == 'audio':
                return True
        return False

    @cached_property
    def duration(self) -> float:
        return float(self.probe_data['format']['duration'])

    @cached_property
    def frame_count(self) -> Union[float, None]:
        if 'nb_frames' in self.video_stream:
            return float(self.video_stream['nb_frames'])
        else:
            return None


def is_animated_sequence(data: bytes) -> bool:
    buf = io.BytesIO(data)
    pil_img = PILImage.open(buf, formats=None)
    return pil_img.is_animated


def guess_mimetype(data: bytes) -> str:
    magic = Magic(mime=True)
    return magic.from_buffer(data)
