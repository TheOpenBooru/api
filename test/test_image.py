"""
- Downscale Resolution
 - Resolution Cap on Both Sides is Accurate
 - 
- Image Parsing
 - Test
"""
from modules.image import Image,Dimensions,calculate_downscale,generateThumbnail,process
import unittest


with open('./data/images/EmptyProfile.webp','rb') as f:
    EXAMPLE_IMAGE = f.read()


class test_Calculate_Downscale(unittest.TestCase):
    def test_Resolution_Is_Smaller_Than_Target(self):
        res = Dimensions(8,2)
        target = Dimensions(10,10)
        actual = calculate_downscale(res,target)
        expected = Dimensions(8,2)
        self.assertEqual(actual,expected)
    
    def test_Height_Is_Larger_Than_Target(self):
        res = Dimensions(10,20)
        target = Dimensions(10,10)
        actual = calculate_downscale(res,target)
        expected = Dimensions(5,10)
        self.assertEqual(actual,expected)

    def test_Width_Is_Larger_Than_Target(self):
        res = Dimensions(20,10)
        target = Dimensions(10,10)
        actual = calculate_downscale(res,target)
        expected = Dimensions(10,5)
        self.assertEqual(actual,expected)

    def test_Both_Are_Larger_Than_Target(self):
        res = Dimensions(500,500)
        target = Dimensions(10,10)
        actual = calculate_downscale(res,target)
        expected = Dimensions(10,10)
        self.assertEqual(actual,expected)


class test_Image_Processing(unittest.TestCase):
    def test_a(self):
        img = Image(EXAMPLE_IMAGE)
        len(img.data)
        dimensions = Dimensions(100,100)
        processed_image = process(img,dimensions,50)
        processed_image.resolution = dimensions
        self.assertLess(len(processed_image.data),len(img.data))
        