from modules import settings
from modules.encoding import Image, ImageFile
import io
import json
import unittest
from typing import Union
from box import Box
from pathlib import Path
from PIL import Image as PILImage



with open('data/test/sample_data.json') as f:
    _json = json.load(f)
    box_data = Box(_json['image'])

class TestData:
    Small = box_data.Small.file
    Massive = box_data.Massive.file
    Complex = box_data.Complex.file
    Landscape = box_data.Landscape.file


class OutputLocation:
    full = Path("./data/storage/image_full.webp")
    preview = Path("./data/storage/image_preview.webp")
    thumbnail = Path("./data/storage/image_thumbnail.webp")


def load_image(path:Union[str,Path]) -> tuple[ImageFile,ImageFile,ImageFile]:
    with open(path,'rb') as f:
        with Image(f.read()) as img:
            full = img.full()
            preview = img.preview()
            thumbnail = img.thumbnail()
    return full,preview,thumbnail


class test_Resolutions_are_Correct(unittest.TestCase):
    def test_Small_Image_Doesnt_Change_Size(self):
        variations = load_image(TestData.Small)
        for x in variations:
            assert x.height == 5 and x.width == 5, f"Full: {x.height}x{x.width} is not 5x5"
    
    def test_Aspect_Ratio_is_Reserved(self):
        og_ratio = box_data.Landscape.height / box_data.Landscape.width
        variations = load_image(TestData.Landscape)
        for x in variations:
            new_ratio = x.height/x.width
            self.assertAlmostEqual(
                first=og_ratio,second=new_ratio,delta=0.01,
                msg=f"Original: {new_ratio}\nNew:{og_ratio}"
            )


class test_Images_Too_Large_Raise_Error(unittest.TestCase):
    def test_Images_Too_Large_Raise_Error(self):
        with open(TestData.Massive,'rb') as f:
            data = f.read()
        with self.assertRaises(ValueError):
            with Image(data) as img:
                pass

class test_Create_Full(unittest.TestCase):
    full: ImageFile
    def setUp(self):
        with open(TestData.Landscape,'rb') as f:
            with Image(f.read()) as img:
                self.full = img.full()

    def load_PIL(self):
        buf = io.BytesIO(self.full.data)
        return PILImage.open(buf,formats=None)
    
    def test_Full_Is_Valid(self):
        PIL = self.load_PIL()
        PIL.verify()
    
    def test_Full_Save_Example(self):
        PIL = self.load_PIL()
        PIL.save(OutputLocation.full)
    


class test_Create_Preview(unittest.TestCase):
    preview: ImageFile
    def setUp(self):
        with open(TestData.Complex,'rb') as f:
            with Image(f.read()) as img:
                self.preview = img.preview()
    
    def test_Preview_can_be_loaded(self): 
        buf = io.BytesIO(self.preview.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save(OutputLocation.preview)
    
    
    def test_Preview_Is_Correct_Resolution(self):
        preview = self.preview
        max_height = settings.IMAGE_PREVIEW_HEIGHT
        max_width = settings.IMAGE_PREVIEW_WIDTH
        
        assert (preview.width == max_width) or (preview.height == max_height), "Image Preview Height or Width is not correct"
    
    
    def test_Small_Image_Doesnt_Change_Size(self):
        preview = load_image(TestData.Small)[1]
        assert preview.height == 5, "Preview Height increased"
        assert preview.width == 5, "Preview Width increased"


class test_Create_Thumbnail(unittest.TestCase):
    thumbnail: ImageFile
    def setUp(self):
        with open(TestData.Complex,'rb') as f:
            with Image(f.read()) as img:
                self.thumbnail = img.thumbnail()
    
    def test_Thumbnail_can_be_loaded(self): 
        buf = io.BytesIO(self.thumbnail.data)
        pil_img = PILImage.open(buf,formats=None)
        pil_img.verify()
        pil_img.save(OutputLocation.thumbnail)
    
    
    def test_Thumbnail_Is_Correct_Resolution(self):
        thumbnail = self.thumbnail
        max_height = settings.THUMBNAIL_HEIGHT
        max_width = settings.THUMBNAIL_WIDTH
        
        res_delta = thumbnail.width - max_width, thumbnail.height == max_height
        assert 0 in res_delta,f"Image Thumbnail Height or Width is not correct: {res_delta}"
    
    
    def test_Small_Image_Doesnt_Change_Size(self):
        thumbnail = load_image(TestData.Small)[2]
        assert thumbnail.height == 5, f"{thumbnail.height}"
        assert thumbnail.width == 5, f"{thumbnail.width}"
