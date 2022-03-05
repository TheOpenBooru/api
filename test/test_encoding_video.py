import io
from pathlib import Path
from modules import settings
from modules.encoding import Video,VideoFile,ImageFile
import unittest
import asyncio
from PIL import Image as PILImage

class TestData:
    sea = Path("./data/test/video/Sea.mp4")

class OutputPaths:
    full = Path("./data/files/video_full.mp4")
    preview = Path("./data/files/video_preview.mp4")
    thumbnail = Path("./data/files/video_thumbnail.webp")


def load_video(path) -> Video:
    with open(path,'rb') as f:
        data = f.read()
    coroutine = Video.from_bytes(data)
    return asyncio.run(coroutine)

class test_Video_Full(unittest.TestCase):
    video:Video
    full:VideoFile
    def setUp(self):
        self.video = load_video(TestData.sea)
        self.full = asyncio.run(self.video.full())
    
    def test_Save_Example(self):
        with open(OutputPaths.full,'wb') as f:
            f.write(self.full.data)
    
    def test_Metadata_Is_Valid(self):
        assert self.full.width == 1920
        assert self.full.height == 1080
        assert self.full.frame_count == 729
        assert self.full.hasAudio == True
        assert self.full.mimetype == 'video/mp4'
        
        self.assertAlmostEqual(self.full.duration,24.323,places=3)
        self.assertAlmostEqual(self.full.framerate,29.97,places=2)

# class test_Video_Preview(unittest.TestCase):
#     video:Video
#     preview:VideoFile
#     def setUp(self):
#         self.video = load_video(TestData.mp4)
#         self.preview = asyncio.run(self.video.preview())
    
#     def test_Save_Example(self):
#         with open(Output.preview,'wb') as f:
#             f.write(self.preview.data)


class test_Video_Thumbnail(unittest.TestCase):
    video:Video
    thumbnail:ImageFile
    def setUp(self):
        self.video = load_video(TestData.sea)
        self.thumbnail = asyncio.run(self.video.thumbnail())
    
    def test_Save_Example(self):
        with open(OutputPaths.thumbnail,'wb') as f:
            f.write(self.thumbnail.data)
