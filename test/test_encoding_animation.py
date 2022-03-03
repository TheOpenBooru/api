import io
from modules import settings
from modules.encoding import Animation,AnimationFile,ImageFile
import unittest
import asyncio
from PIL import Image as PILImage

class TestData:
    gif = "./data/test/animation/500x500-50ms.gif"
    webp = "data/test/animation/500x500-50ms.webp"
    single_frame = "data/test/image/SingleFrame.gif"

def load_animation(path) -> Animation: 
    with open(path,'rb') as f:
        return asyncio.run(Animation.from_bytes(f.read()))


class test_Animations_Require_More_Than_One_Frame(unittest.TestCase):
    def test_a(self):
        with open(TestData.single_frame, "rb") as f:
            data = f.read()
        coroutine = Animation.from_bytes(data)
        self.assertRaises(ValueError, asyncio.run, coroutine)


class test_GIF(unittest.TestCase):
    animation:Animation
    def setUp(self) -> None:
        self.animation = load_animation(TestData.gif)
        
        self.full = asyncio.run(self.animation.full())
        self.preview = asyncio.run(self.animation.preview())
        self.thumbnail = asyncio.run(self.animation.thumbnail())


    def test_Full_Is_Valid(self):
        assert isinstance(self.full,AnimationFile), "Did not generate a full version correctly"
        buf = io.BytesIO(self.full.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        assert self.full.frame_count == pil_img.n_frames, "Number of frames is not correct"
        assert self.full.duration == 0.6, "File Duration is incorrect"
        pil_img.save('./data/images/animation_full.webp')


    def test_Preview_isnt_Generated(self):
        assert self.preview == None, "Generated a preview image"


    def test_Thumbnail_is_Valid(self):
        assert isinstance(self.thumbnail,ImageFile), "Did not generate a thumbnail version correctly"
        buf = io.BytesIO(self.full.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        assert isinstance(self.thumbnail,ImageFile), "Did not generate a thumbnail version correctly"
        pil_img.save('./data/images/animation_thumbnail.webp')

