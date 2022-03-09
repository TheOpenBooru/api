from datetime import datetime
from . import VideoFile,ImageFile,BaseMedia,Image
from modules import settings
import os
import time
import random
from typing import Any
from dataclasses import dataclass
import ffmpeg
from magic import Magic

@dataclass
class Video(BaseMedia):
    type="video"
    _data:bytes
    _mimetype:str
    _width:int
    _height:int
    _hasAudio:bool
    _framerate:float
    _frame_count:int
    _duration:float

    @classmethod
    async def from_bytes(cls, data):
        video_data:dict = get_video_data(data)
        return Video(
            _data=data,
            **video_data
        )

    async def full(self) -> VideoFile:
        return VideoFile(
            data=self._data,
            mimetype=self._mimetype,
            width=self._width,
            height=self._height,
            frame_count=self._frame_count,
            framerate=self._framerate,
            duration=self._duration,
            hasAudio=self._hasAudio,
        )

    async def preview(self) -> None:
        return None

    async def thumbnail(self) -> ImageFile:
        seek_percent = settings.get('encoding.video.thumbnail.timing_percent')
        seek_time = (self._duration / 100) * seek_percent
        try:
            process = (
                ffmpeg
                .input('pipe:')
                .output("pipe:",format="image2",ss=seek_time,**{"frames:v":1 })
                .run(input=self._data,capture_stdout=True,capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise ValueError(f"FFmpeg could not parse: {e.stderr}")
        data = process[0]
        img = await Image.from_bytes(data)
        return await img.thumbnail()


def get_video_data(data:bytes) -> dict:
    ffprobe_data = ffprobe(data)
    video_stream = get_video_stream(ffprobe_data)
    metadata = {}
    metadata["_mimetype"] = get_mimetype(data)
    metadata["_hasAudio"] = has_audio(ffprobe_data)
    metadata["_duration"] = get_duration(ffprobe_data,video_stream)
    metadata["_frame_count"] = get_frame_count(video_stream)
    metadata["_width"] = int(video_stream['width'])
    metadata["_height"] = int(video_stream['height'])
    metadata["_framerate"] = eval(video_stream['avg_frame_rate'])
    return metadata


def ffprobe(data:bytes) -> dict:
    return generate_temporary_file(data,ffmpeg.probe)

def generate_temporary_file(data:bytes,callback) -> Any:
    rand = hex(random.randint(0,2**64))
    filepath = f"/tmp/openbooru_{rand}"
    
    with open(filepath,'wb') as f:
        f.write(data)
    output:dict = callback(filepath)
    os.remove(filepath)
    return output

def get_video_stream(ffprobe_data:dict) -> dict:
    for stream in ffprobe_data['streams']:
        if stream['codec_type'] == 'video':
            return stream
    raise ValueError("No video stream found")

def get_mimetype(data) -> str:
    return Magic(mime=True).from_buffer(data)

def has_audio(ffprobe_data:dict) -> bool:
    for stream in ffprobe_data['streams']:
        if stream['codec_type'] == 'audio':
            return True
    return False

def get_duration(ffprobe_data:dict,video_stream:dict) -> float:
    if 'duration' in video_stream:
        return float(video_stream['duration'])
    elif video_stream['codec_name'] == 'vp8':
        return float(ffprobe_data['duration'])
    else:
        raise ValueError("Unsupported video format")

def get_frame_count(video_stream:dict) -> float:
    if 'duration' in video_stream:
        return float(video_stream['nb_frames'])
    elif video_stream['codec_name'] == 'vp8':
        raise NotImplementedError("VP8 does not support frame count")
    else:
        raise ValueError("Unsupported video format")