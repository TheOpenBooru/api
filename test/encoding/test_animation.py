from openbooru.modules import settings
from openbooru.modules.encoding import AnimationEncoder, AnimationFile, ImageFile
import io
import json
from box import Box
import unittest
import asyncio
from PIL import Image as PILImage

with open('data/test/sample_data.json') as f:
    _json = json.load(f)
    TestData = Box(_json['animation'])


class OutputLocation:
    full = "./data/storage/animation_full.webp"
    thumbnail = "./data/storage/animation_thumbnail.webp"


def load_PIL_from_data(data) -> PILImage.Image:
    buf = io.BytesIO(data)
    return PILImage.open(buf)


class test_Animations_Require_More_Than_One_Frame(unittest.TestCase):
    def test_a(self):
        with open(TestData.SingleFrame.file, "rb") as f:
            data = f.read()
        self.assertRaises(ValueError, AnimationEncoder, data)


@unittest.skip("TODO: https://trello.com/c/p5Fv7jne/106-bug-fix-gif-encoding-strips-transparency")
class test_Animations_Preserve_Transparency(unittest.TestCase):
    def setUp(self) -> None:
        with open(TestData.Transparent.file, 'rb') as f:
            with AnimationEncoder(f.read()) as anim:
                full = anim.original()
            self.PIL = load_PIL_from_data(full.data)

    def test_Animations_Preserve_Transparency(self):
        PIL = self.PIL
        for x in range(PIL.n_frames):
            PIL.seek(x)
            RGB_MinMax_Values = PIL.getextrema()
            MaxTransparency = RGB_MinMax_Values[3][0]
            assert MaxTransparency != 255, f"Frame {x} is not transparent"


class test_Animation_Full(unittest.TestCase):
    def setUp(self) -> None:
        self.original_file = TestData.Transparent.file
        with open(TestData.Transparent.file, 'rb') as f:
            with AnimationEncoder(f.read()) as anim:
                self.full = anim.original()

    def test_Is_AnimationFile(self):
        assert isinstance(
            self.full, AnimationFile), "Did not generate a full version correctly"

    def test_Full_Is_Valid(self):
        PIL = load_PIL_from_data(self.full.data)
        PIL.verify()
        assert PIL.is_animated, "Did not save as animation"

    def test_Attributes_are_Correct(self):
        assert self.full.frame_count == 128, f"Number of frames is not correct: {self.full.frame_count}"
        assert self.full.duration == 6.4, f"File Duration is incorrect: {self.full.duration}"

    def test_Save_Example_Image(self):
        PIL = load_PIL_from_data(self.full.data)
        PIL.save(OutputLocation.full, save_all=True)


class test_Animation_Preview(unittest.TestCase):
    def setUp(self) -> None:
        self.original_file = TestData.Transparent.file
        with open(TestData.Transparent.file, 'rb') as f:
            with AnimationEncoder(f.read()) as anim:
                self.preview = anim.preview()

    def test_Preview_isnt_Generated(self):
        assert isinstance(
            self.preview, ImageFile), "Animation Preview is not an Image"


class test_Animation_Thumbnail(unittest.TestCase):
    def setUp(self) -> None:
        self.original_file = TestData.Transparent.file
        with open(TestData.Transparent.file, 'rb') as f:
            with AnimationEncoder(f.read()) as anim:
                self.thumbnail = anim.thumbnail()
                self.data = self.thumbnail.data

    def test_Thumbnail_is_ImageFile(self):
        assert isinstance(
            self.thumbnail, ImageFile), "Did not generate a thumbnail version correctly"

    def test_Thumbnail_Is_Correct_Resolution(self):
        max_width = settings.THUMBNAIL_WIDTH
        max_height = settings.THUMBNAIL_HEIGHT
        width, height = self.thumbnail.width, self.thumbnail.height
        assert (width == max_width) or (
            height == max_height), f"Thumbnail is not the correct resolution: {width}x{height}"

    def test_Thumbnail_Is_Valid(self):
        PIL = load_PIL_from_data(self.data)
        PIL.verify()

    def test_Save_Example(self):
        PIL = load_PIL_from_data(self.data)
        PIL.save(OutputLocation.thumbnail)
