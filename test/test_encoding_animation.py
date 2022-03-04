from modules import settings
from modules.encoding import Animation,AnimationFile,ImageFile
import io
import unittest
import asyncio
from PIL import Image as PILImage

class TestData:
    gif = "./data/test/animation/500x500-50ms-12frames.gif"
    webp = "data/test/animation/500x500-50ms-12frames.webp"
    single_frame = "data/test/image/SingleFrame.gif"

class OutputLocation:
    full = "./data/files/animation_full.webp"
    thumbnail = "./data/files/animation_thumbnail.webp"

def load_animation(path) -> Animation: 
    with open(path,'rb') as f:
        return asyncio.run(Animation.from_bytes(f.read()))


class test_Animations_Require_More_Than_One_Frame(unittest.TestCase):
    def test_a(self):
        with open(TestData.single_frame, "rb") as f:
            data = f.read()
        coroutine = Animation.from_bytes(data)
        self.assertRaises(ValueError, asyncio.run, coroutine)


class test_Animation_Full(unittest.TestCase):
    def setUp(self) -> None:
        self.original_file = TestData.gif
        self.animation = load_animation(TestData.gif)
        self.full = asyncio.run(self.animation.full())

    def load_PIL(self):
        buf = io.BytesIO(self.full.data)
        return PILImage.open(buf,formats=None)

    def test_Is_AnimationFile(self):
        assert isinstance(self.full,AnimationFile), "Did not generate a full version correctly"
    
    def test_Full_Is_Valid(self):
        PIL = self.load_PIL()
        PIL.verify()
    
    def test_Attributes_are_Correct(self):
        PIL = PILImage.open(self.original_file)
        assert self.full.frame_count == PIL.n_frames, f"Number of frames is not correct: {self.full.frame_count}"
        assert self.full.duration == 0.6, "File Duration is incorrect"
    
    def test_Save_Example_Image(self):
        PIL = self.load_PIL()
        PIL.save(OutputLocation.full,save_all=True)


class test_Animation_Preview(unittest.TestCase):
    def setUp(self) -> None:
        self.animation = load_animation(TestData.gif)
        self.preview = asyncio.run(self.animation.preview())

    def test_Preview_isnt_Generated(self):
        assert self.preview == None, "Generated a preview image"


class test_Animation_Thumbnail(unittest.TestCase):
    def setUp(self) -> None:
        self.animation = load_animation(TestData.gif)
        self.thumbnail = asyncio.run(self.animation.thumbnail())
        self.data = self.thumbnail.data


    def load_PIL(self):
        buf = io.BytesIO(self.data)
        return PILImage.open(buf,formats=None)


    def test_Thumbnail_is_ImageFile(self):
        assert isinstance(self.thumbnail,ImageFile), "Did not generate a thumbnail version correctly"


    def test_Thumbnail_Is_Correct_Resolution(self):
        max_width = settings.get('encoding.image.thumbnail.max_height')
        max_height = settings.get('encoding.image.thumbnail.max_width')
        width,height = self.thumbnail.width, self.thumbnail.height
        assert (width == max_width) or (height == max_height), f"Thumbnail is not the correct resolution: {width}x{height}"
    
    def test_Thumbnail_Is_Valid(self):
        PIL = self.load_PIL()
        PIL.verify()

    def test_Save_Example(self):
        PIL = self.load_PIL()
        PIL.save(OutputLocation.thumbnail)
