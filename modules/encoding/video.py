from . import VideoFile,ImageFile,MediaBase
from modules import settings
from cachetools import cached,Cache
from dataclasses import dataclass
import json
import ffmpeg
import subprocess

@dataclass
class Video(MediaBase):
    data:bytes
    mimetype:str
    width:int
    height:int
    hasAudio:bool
    framerate:float
    frame_count:int
    duration:float

    @classmethod
    async def from_bytes(cls, data):
        raise NotImplementedError("Videos aren't supported yet")
        mimetype = get_mimetype(data)
        
        metadata = ffprobe(data)
        stream_data:dict = metadata['streams'][0]
        hasAudio = len(metadata) == 2
        framerate = eval(stream_data['avg_frame_rate'])
        return Video(
            data=data,
            mimetype=mimetype,
            width=stream_data['width'],
            height=stream_data['height'],
            hasAudio=hasAudio,
            duration=stream_data['duration'],
            frame_count=stream_data['nb_frames'],
            framerate=framerate,
        )

    async def full(self) -> VideoFile:
        ffmpeg_params = settings.get('encoding.video.ffmpeg_args')
        process = (
            ffmpeg
            .input('pipe:')
            .output('pipe:',**ffmpeg_params)
            .run()
        )
        process.stdin.write(self.data)
        data = process.stdout.read()
        return VideoFile(
            data=data,
            mimetype='video/mp4',
            width=self.width,
            height=self.height,
            frame_count=self.frame_count,
            framerate=self.framerate,
            duration=self.duration,
            hasAudio=self.hasAudio,
            )

    async def preview(self) -> VideoFile:
        ...

    async def thumbnail(self) -> ImageFile:
        ...


def get_mimetype(data) -> str:
    return 'video/mp4'

def ffprobe(data:bytes) -> dict:
    process = subprocess.Popen([ 
        "ffprobe",
        "-v","quiet",
        "-print_format","json",
        "-show_format","-show_streams",
        "pipe:"
    ])
    process.stdin.write(data) # type: ignore
    json_data = process.stdout.read() # type: ignore
    json_text = json_data.decode()
    metadata = json.loads(json_text)
    return metadata