import io
from modules import settings
from modules.encoding import Image, ImageFile
import unittest
import asyncio
from PIL import Image as PILImage

class TestData:
    Complex = "./data/test/image/Complex.webp"
    Large = "./data/test/image/Large.webp"
    Small = "./data/test/image/5x5.webp"
    Landscape = "./data/test/image/Landscape.webp"


def load_image(path) -> Image: 
    with open(path,'rb') as f:
        data = f.read()
    coroutine = Image.from_bytes(data)
    return asyncio.run(coroutine)


class test_Create_Thumbnail(unittest.TestCase):
    thumbnail: ImageFile
    def setUp(self):
        image = load_image(TestData.Complex)
        self.thumbnail = asyncio.run(image.thumbnail())
    
    def test_Thumbnail_can_be_loaded(self): 
        buf = io.BytesIO(self.thumbnail.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save('./data/images/image_thumbnail.webp')
    
    
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


class test_Create_Preview(unittest.TestCase):
    preview: ImageFile
    def setUp(self):
        image = load_image(TestData.Complex)
        self.preview = asyncio.run(image.preview())
    
    def test_Preview_can_be_loaded(self): 
        buf = io.BytesIO(self.preview.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save('./data/images/image_preview.webp')
    
    
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



class test_Create_Full(unittest.TestCase):
    full: ImageFile
    def setUp(self):
        image = load_image(TestData.Large)
        self.full = asyncio.run(image.full())
    
    def test_Full_can_be_loaded(self):
        image = load_image(TestData.Complex)
        self.full = asyncio.run(image.full())
        buf = io.BytesIO(self.full.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save('./data/images/image_full.webp')
    
    
    def test_Full_Is_Correct_Resolution(self):
        image = load_image(TestData.Landscape)
        full = asyncio.run(image.full())
        
        config = settings.get('encoding.image.full')
        max_height,max_width = config['max_height'],config['max_width']
        
        assert (full.width == max_width) or (full.height == max_height), "Image Full Height or Width is not correct"
    
    
    def test_Small_Image_Doesnt_Change_Size(self):
        small_image = load_image(TestData.Small)
        full = asyncio.run(small_image.full())
        
        assert full.height == 5, "Full Height increased"
        assert full.width == 5, "Full Width increased"