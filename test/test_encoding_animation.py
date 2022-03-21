from modules import settings
from modules.encoding import Animation,AnimationFile,ImageFile
import io
import unittest
import asyncio
from PIL import Image as PILImage
 
class OutputLocation:
    full = "./data/files/animation_full.webp"
    thumbnail = "./data/files/animation_thumbnail.webp"

def load_animation(path) -> Animation: 
    with open(path,'rb') as f:
        data = f.read()
    return Animation(data)

def load_PIL_from_data(data) -> PILImage.Image:
    buf = io.BytesIO(data)
    return PILImage.open(buf)

class test_Animations_Require_More_Than_One_Frame(unittest.TestCase):
    def test_a(self):
        with open(TestData.single_frame, "rb") as f:
            data = f.read()
        self.assertRaises(ValueError, Animation(data))


class test_Animations_Preserve_Transparency(unittest.TestCase):
    def setUp(self) -> None:
        self.original_file = TestData.transparent
        self.animation = load_animation(TestData.transparent)
        self.full = asyncio.run(self.animation.full())
    
    def test_Animations_Preserve_Transparency(self):
        PIL = load_PIL_from_data(self.full.data)
        for x in range(PIL.n_frames):
            PIL.seek(x)
            MinMax_Channel_Values = PIL.getextrema()
            _,_,_,(a_min,a_max) = MinMax_Channel_Values
            assert a_min != 255, f"Frame {x} is not transparent"


class test_Animation_Full(unittest.TestCase):
    def setUp(self) -> None:
        self.original_file = TestData.transparent
        self.animation = load_animation(TestData.transparent)
        coroutine = self.animation.full()
        self.full = asyncio.run(coroutine)

    def test_Is_AnimationFile(self):
        assert isinstance(self.full,AnimationFile), "Did not generate a full version correctly"
    
    def test_Full_Is_Valid(self):
        PIL = load_PIL_from_data(self.full.data)
        PIL.verify()
    
    def test_Attributes_are_Correct(self):
        PIL = PILImage.open(self.original_file)
        assert self.full.frame_count == 128, f"Number of frames is not correct: {self.full.frame_count}"
        assert self.full.duration == 6.4, f"File Duration is incorrect: {self.full.duration}"
    
    def test_Save_Example_Image(self):
        PIL = load_PIL_from_data(self.full.data)
        PIL.save(OutputLocation.full,save_all=True)


class test_Animation_Preview(unittest.TestCase):
    def setUp(self) -> None:
        self.animation = load_animation(TestData.transparent)
        self.preview = asyncio.run(self.animation.preview())

    def test_Preview_isnt_Generated(self):
        assert self.preview == None, "Generated a preview image"


class test_Animation_Thumbnail(unittest.TestCase):
    def setUp(self) -> None:
        self.animation = load_animation(TestData.transparent)
        self.thumbnail = asyncio.run(self.animation.thumbnail())
        self.data = self.thumbnail.data

    def test_Thumbnail_is_ImageFile(self):
        assert isinstance(self.thumbnail,ImageFile), "Did not generate a thumbnail version correctly"

    def test_Thumbnail_Is_Correct_Resolution(self):
        max_width = settings.get('encoding.image.thumbnail.max_height')
        max_height = settings.get('encoding.image.thumbnail.max_width')
        width,height = self.thumbnail.width, self.thumbnail.height
        assert (width == max_width) or (height == max_height), f"Thumbnail is not the correct resolution: {width}x{height}"
    
    def test_Thumbnail_Is_Valid(self):
        PIL = load_PIL_from_data(self.data)
        PIL.verify()

    def test_Save_Example(self):
        PIL = load_PIL_from_data(self.data)
        PIL.save(OutputLocation.thumbnail)
