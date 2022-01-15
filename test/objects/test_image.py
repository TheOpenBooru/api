from . import LOOKUP,DATA,clear
from . import Image
import unittest

class test_Create_Image(unittest.TestCase):
    def setUp(self):
        clear()

    def test_Create_Image(self):
        data = DATA.IMAGE
        imgID = Image.create(**data)
        self.assertIsInstance(imgID,int,"Didn't return interger ID")
        img = Image.get(md5=data["md5"])
        self.assertDictContainsSubset(data, img)

        for key,value in img.items():
            self.assertIn(key,LOOKUP.IMAGE,f"Invalid Key '{key}' inside Image")
            self.assertIsInstance(value,LOOKUP.IMAGE[key])
