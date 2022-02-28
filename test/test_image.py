"""
- Downscale Resolution
 - Resolution Cap on Both Sides is Accurate
 - 
- Image Parsing
 - Test
"""
from modules import image,settings
import unittest

class test_Calculate_Downscale(unittest.TestCase):
    def test_Resolution_Is_Smaller_Than_Target(self):
        res = image.Dimensions(8,2)
        target = image.Dimensions(10,10)
        actual = image.calculate_downscale(res,target)
        expected = image.Dimensions(8,2)
        assert actual == expected
    
    def test_Resolution_Is_Larger_Than_Target(self):
        res = image.Dimensions(500,500)
        target = image.Dimensions(10,10)
        actual = image.calculate_downscale(res,target)
        expected = image.Dimensions(10,10)
        assert actual == expected
    
    def test_Height_Is_Larger_Than_Target(self):
        res = image.Dimensions(10,20)
        target = image.Dimensions(10,10)
        actual = image.calculate_downscale(res,target)
        expected = image.Dimensions(5,10)
        assert actual == expected

    def test_Width_Is_Larger_Than_Target(self):
        res = image.Dimensions(20,10)
        target = image.Dimensions(10,10)
        actual = image.calculate_downscale(res,target)
        expected = image.Dimensions(10,5)
        assert actual == expected


class test_Image_From_File(unittest.TestCase):
    def test_Extention_is_Preserved(self):
        with open('./data/images/test_Fractal.webp','rb') as f:
            img = image.file_to_image(f)
        assert img.format == 'WEBP', img.format
    
    def test_Original_Data_is_Preserved(self):
        with open('./data/images/test_Fractal.webp','rb') as f:
            source_data = f.read()
        with open('./data/images/test_Fractal.webp','rb') as f:
            img = image.file_to_image(f)
        assert img.data == source_data


class test_Image_Processing(unittest.TestCase):
    def test_Resize_Downscales_to_Correct_Resolution(self):
        with open('./data/images/test_Fractal.webp','rb') as f:
            img = image.file_to_image(f)
        dimensions = image.Dimensions(100,100)
        processed_image = image.process(img,dimensions,100)
        assert processed_image.resolution == dimensions
    
    def test_Process_Reduces_Image_Size(self):
        with open('./data/images/test_Fractal.webp','rb') as f:
            source_data = f.read()
        with open('./data/images/test_Fractal.webp','rb') as f:
            img = image.file_to_image(f)
        processed_image = image.process(img,img.resolution,50)
        assert len(processed_image.data) < len(source_data)


class test_Create_Thumbnail(unittest.TestCase):
    def test_Thumbnail_Is_Correct_Resolution(self):
        with open('./data/images/test_Fractal.webp','rb') as f:
            img = image.file_to_image(f)
        thumbnail = image.generateThumbnail(img)
        height = settings.get('settings.posts.thumbnail.max_height')
        width = settings.get('settings.posts.thumbnail.max_width')
        res = thumbnail.resolution
        error_msg = f"{res.width}x{res.height}"
        assert res.width == width or res.height == height, error_msg
    
    def test_Small_Image_Doesnt_Change_Size(self):
        with open('./data/images/test_Small.webp','rb') as f:
            img = image.file_to_image(f)
        thumbnail = image.generateThumbnail(img)
        assert thumbnail.resolution.height == 5
        assert thumbnail.resolution.width == 5


class test_Create_Preview(unittest.TestCase):
    def test_Preview_Is_Correct_Resolution(self):
        with open('./data/images/test_Fractal.webp','rb') as f:
            img = image.file_to_image(f)
        Preview = image.generatePreview(img)
        config = settings.get('settings.posts.preview')
        height = config['max_height']
        width = config['max_width']
        res = Preview.resolution
        error_msg = f"{res.width}x{res.height}"
        assert res.width == width or res.height == height, error_msg
    
    def test_Small_Image_doesnt_Change_Size(self):
        with open('./data/images/test_Small.webp','rb') as f:
            img = image.file_to_image(f)
        preview = image.generatePreview(img)
        assert preview.resolution.height == 5
        assert preview.resolution.width == 5


class test_Create_Full(unittest.TestCase):
    def test_Full_Is_Correct_Resolution(self):
        with open('./data/images/test_Large.webp','rb') as f:
            img = image.file_to_image(f)
        Preview = image.generateFull(img)
        config = settings.get('settings.posts.full')
        height = config['max_height']
        width = config['max_width']
        res = Preview.resolution
        error_msg = f"{res.width}x{res.height}"
        assert res.width == width or res.height == height, error_msg
    
    def test_Small_Image_doesnt_Change_Size(self):
        with open('./data/images/test_Small.webp','rb') as f:
            img = image.file_to_image(f)
        preview = image.generateFull(img)
        assert preview.resolution.height == 5
        assert preview.resolution.width == 5