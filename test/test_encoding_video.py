from modules.encoding.types import ImageFile
from modules.encoding import Video
import unittest
from box import Box
import json

with open('data/test/sample_data.json') as f:
    _json = json.load(f)
    test_data = Box(_json['video'])


class test_Heavy(unittest.TestCase):
    def setUp(self):
        self.info = test_data.heavy
        with open(self.info.file,'rb') as f:
            data = f.read()
        self.video = Video(data)

    
    def test_Preview_Isnt_Generated(self):
        with self.video as v:
            assert v.preview() == None

    
    def test_Thumbnail_is_Image(self):
        with self.video as v:
            thumbnail = v.thumbnail()
        assert type(thumbnail) == ImageFile

    
    def test_Video_Metadata_Is_Correct(self):
        with self.video as v:
            full = v.full()
        assert full.height == self.info.height, full.height
        assert full.width == self.info.width, full.width
        assert full.framerate == self.info.framerate, full.framerate
        self.assertAlmostEqual(full.duration, self.info.duration, delta=0.1)
        assert full.mimetype == self.info.mimetype, full.mimetype
        assert full.hasAudio == self.info.hasAudio, full.hasAudio
