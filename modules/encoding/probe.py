from functools import cached_property
import mimetypes
import warnings
from magic import Magic
import ffmpeg

class Probe:
    filepath:str
    data:bytes
    def __init__(self,filepath:str):
        ...
    

class VideoProbe(Probe):
    def __init__(self,filepath):
        with open(filepath,'rb') as f:
            self.data = f.read()
        self.filepath = filepath
        self.probe_data = ffmpeg.probe(self.filepath)


    @cached_property
    def _video_stream(self) -> dict:
        streams = self.probe_data['streams']
        video_streams = [x for x in streams if x['codec_type'] == 'video']
        if len(video_streams) == 1:
            return video_streams[0]
        else:
            raise Exception('No or Multiple Video Streams Found')
    
    @cached_property
    def height(self) -> int:
        return self._video_stream['height']
    
    @cached_property
    def width(self) -> int:
        return self._video_stream['width']

    @cached_property
    def framerate(self) -> str:
        framerate = eval(self._video_stream['r_frame_rate'])
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
        if ext != None:
            return ext
        else:
            raise Exception("Couldn't Guess File Extention")

    @cached_property
    def audio(self) -> bool:
        for stream in self.probe_data['streams']:
            if stream['codec_type'] == 'audio':
                return True
        return False

    @cached_property
    def duration(self) -> float:
        if 'duration' in self._video_stream:
            return float(self._video_stream['duration'])
        elif self._video_stream['codec_name'] in ['vp8','vp9']:
            return float(self.probe_data['format']['duration'])
        else:
            raise ValueError("Unsupported video format")

    @cached_property
    def frame_count(self) -> float:
        if 'nb_frames' in self._video_stream:
            return float(self._video_stream['nb_frames'])
        else:
            return int (eval(self.framerate) * self.duration * 0.9)


class ImageProbe(Probe):
    def __init__(self,filepath):
        self.filepath = filepath
        with open(filepath,'rb') as f:
            self.data = f.read()

    @cached_property
    def extention(self) -> str:
        return "jpg"