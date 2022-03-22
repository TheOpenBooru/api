import json
import asyncio
import unittest
from box import Box
from modules.encoding import predict_media_type,Animation,Image,Video,BaseMedia

with open('data/test/sample_data.json') as f:
    _json = json.load(f)
    test_data = Box(_json)

class TestData:
    MP4_Video = test_data.video.heavy.file
    WEBP_Animation = test_data.animation.Transparent.file
    WEBP_Image = test_data.image.Complex.file
    GIF_Animation = test_data.animation.FractalGIF.file
    GIF_Image = test_data.animation.SingleFrame.file


class test_Detect_Format(unittest.TestCase):
    def assertFormat(self,fp:str,type:type,message:str):
        with open(fp,'rb') as f:
            coroutine = predict_media_type(f.read(),fp)
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
