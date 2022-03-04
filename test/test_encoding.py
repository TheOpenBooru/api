# MP4: Video
# WEBM: Video

import asyncio
import unittest
from modules.encoding import generate_media,Animation,Image,Video,MediaBase

class TestData:
    MP4_Video = './data/test/video/Sea.mp4'
    WEBP_Animation = './data/test/animation/500x500-50ms-12frames.webp'
    WEBP_Image = './data/test/image/5x5.webp'
    GIF_Animation = './data/test/animation/500x500-50ms-12frames.gif'
    GIF_Image = './data/test/image/SingleFrame.gif'


class test_Detect_Format(unittest.TestCase):
    def assertFormat(self,fp:str,type:type,message:str):
        with open(fp,'rb') as f:
            coroutine = generate_media(f.read(),fp)
            media_class = asyncio.run(coroutine)
        assert media_class == type, f"message: {media_class.__name__}"
    
    def test_webp_animation(self):
        self.assertFormat(
            TestData.WEBP_Animation,
            Animation,
            "WEBP Animation not recognised"
        )
    
    def test_webp_picture(self):
        self.assertFormat(
            TestData.WEBP_Image,
            Image,
            "WEBP Picutre not recognised",
        )
    
    def test_gif_animation(self):
        self.assertFormat(
            TestData.GIF_Animation,
            Animation,
            "GIF Animation not recognised",
        )
    
    def test_gif_picture(self):
        self.assertFormat(
            TestData.GIF_Image,
            Image,
            "GIF Image not recognised",
        )
    
    def test_mp4_video(self):
        self.assertFormat(
            TestData.MP4_Video,
            Video,
            "MP4 Video not recognised",
        )
