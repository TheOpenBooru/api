import json
import asyncio
import unittest
from box import Box
from modules import schemas
from modules.encoding import generate_encoder, AnimationEncoder, ImageEncoder, VideoEncoder, BaseEncoder

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
    def assertFormat(self, filepath: str, intended_type: schemas.MediaType, message: str):
        with open(filepath, 'rb') as f:
            data = f.read()
        media = asyncio.run(generate_encoder(data, filepath))
        assert media.type == intended_type, message

    def test_webp_animation(self):
        self.assertFormat(
            TestData.WEBP_Animation,
            schemas.MediaType.animation,
            "WEBP Animation not recognised"
        )

    def test_webp_picture(self):
        self.assertFormat(
            TestData.WEBP_Image,
            schemas.MediaType.image,
            "WEBP Picutre not recognised",
        )

    def test_gif_animation(self):
        self.assertFormat(
            TestData.GIF_Animation,
            schemas.MediaType.animation,
            "GIF Animation not recognised",
        )

    def test_gif_picture(self):
        self.assertFormat(
            TestData.GIF_Image,
            schemas.MediaType.image,
            "GIF Image not recognised",
        )

    def test_mp4_video(self):
        self.assertFormat(
            TestData.MP4_Video,
            schemas.MediaType.video,
            "MP4 Video not recognised",
        )
