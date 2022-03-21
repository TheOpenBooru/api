import io
from pathlib import Path
from modules import settings
from modules.encoding import Image, ImageFile
import unittest
import asyncio
from PIL import Image as PILImage


class OutputLocation:
    full = Path("./data/files/image_full.webp")
    preview = Path("./data/files/image_preview.webp")
    thumbnail = Path("./data/files/image_thumbnail.webp")


def load_image(path:str | Path) -> Image: 
    with open(path,'rb') as f:
        data = f.read()
    return Image(data)


class test_Resolutions_are_Correct(unittest.TestCase):
    ...

class test_Landscape_is_Correct(unittest.TestCase):
    full: ImageFile
    def setUp(self):
        image = load_image(TestData.Landscape)
        self.full = asyncio.run(image.full())
    
    def test_Full_Is_Valid(self):
        config = settings.get('encoding.image.full')
        assert self.full.width == config['max_width'], "Landscape Width is not correct"
        assert self.full.height == config['max_height'], "Landscape Height is not correct"

class test_Create_Full(unittest.TestCase):
    full: ImageFile
    def setUp(self):
        image = load_image(TestData.Large)
        self.full = asyncio.run(image.full())

    def load_PIL(self):
        buf = io.BytesIO(self.full.data)
        return PILImage.open(buf,formats=None)
    
    def test_Full_Is_Valid(self):
        PIL = self.load_PIL()
        PIL.verify()
    
    def test_Full_Save_Example(self):
        PIL = self.load_PIL()
        PIL.save(OutputLocation.full)
    
    def test_Small_Image_Doesnt_Change_Size(self):
        small_image = load_image(TestData.Small)
        full = asyncio.run(small_image.full())
        assert full.height == 5 and full.width == 5, f"{full.height}x{full.width} is not 5x5"


class test_Create_Preview(unittest.TestCase):
    preview: ImageFile
    def setUp(self):
        image = load_image(TestData.Complex)
        self.preview = asyncio.run(image.preview())
    
    def test_Preview_can_be_loaded(self): 
        buf = io.BytesIO(self.preview.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save(OutputLocation.preview)
    
    
    def test_Preview_Is_Correct_Resolution(self):
        image = load_image(TestData.Landscape)
        preview = asyncio.run(image.preview())
        
        config = settings.get('encoding.image.preview')
        max_height = config['max_height']
        max_width = config['max_width']
        
        assert (preview.width == max_width) or (preview.height == max_height), "Image Preview Height or Width is not correct"
    
    
    def test_Small_Image_Doesnt_Change_Size(self):
        small_image = load_image(TestData.Small)
        preview = asyncio.run(small_image.preview())
        
        assert preview.height == 5, "Preview Height increased"
        assert preview.width == 5, "Preview Width increased"


class test_Create_Thumbnail(unittest.TestCase):
    thumbnail: ImageFile
    def setUp(self):
        image = load_image(TestData.Complex)
        self.thumbnail = asyncio.run(image.thumbnail())
    
    def test_Thumbnail_can_be_loaded(self): 
        buf = io.BytesIO(self.thumbnail.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save(OutputLocation.thumbnail)
    
    
    def test_Thumbnail_Is_Correct_Resolution(self):
        image = load_image(TestData.Landscape)
        thumbnail = asyncio.run(image.thumbnail())
        config = settings.get('encoding.image.thumbnail')
        max_height = config['max_height']
        max_width = config['max_width']
        
        assert (thumbnail.width == max_width) or (thumbnail.height == max_height), "Image Thumbnail Height or Width is not correct"
    
    
    def test_Small_Image_Doesnt_Change_Size(self):
        small_image = load_image(TestData.Small)
        thumbnail = asyncio.run(small_image.thumbnail())
        
        assert thumbnail.height == 5, "Thumbnail Height increased"
        assert thumbnail.width == 5, "Thumbnail Width increased"
