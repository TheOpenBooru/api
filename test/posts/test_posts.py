from modules import posts, schemas, importing, settings, database, store
import yaml
from unittest import IsolatedAsyncioTestCase as AsyncTestCase

settings.STORAGE_METHOD = 'local'

with open('./data/test/sample_data.json','r') as f:
    TESTDATA = yaml.full_load(f)
    
class test_Post_Create_has_Correct_Attributes(AsyncTestCase):
    async def asyncSetUp(self):
        store.clear()
        database.Post.clear()
    
    async def asyncTearDown(self):
        database.Post.clear()
    
    
    def assert_attributes(self,post:schemas.Post,attrs:dict):
        assert post.full.width == attrs["width"],f'{post.full.width} != {attrs["width"]}'
        assert post.full.height == attrs["height"],f'{post.full.height} != {attrs["height"]}'
        if hasattr(post.full,"duration"):
            self.assertAlmostEqual(post.full.duration,attrs["duration"],places=2) # type: ignore
        if hasattr(post.full,"fps"):
            self.assertEqual(post.full.fps,attrs["framerate"]) # type: ignore
        if hasattr(post.full,"has_sound"):
            self.assertEqual(post.full.has_sound,attrs["hasAudio"]) # type: ignore
            assert post.full.has_sound == attrs["hasAudio"],attrs["hasAudio"] # type: ignore

    
    def load_testdata(self,attrs:dict) -> tuple[bytes,str]:
        filepath = attrs['file']
        attrs.pop('file')
        with open(filepath,'rb') as f:
            data = f.read()
        return data,filepath

    
    async def test_image(self):
        attrs = TESTDATA["image"]["Complex"]
        data,filepath = self.load_testdata(attrs)
        post_obj = await posts.create(data,filepath)
        
        self.assertEqual(post_obj.media_type,"image")
        self.assertIsInstance(post_obj.full,schemas.Image)
        self.assertIsInstance(post_obj.thumbnail,schemas.Image)
        self.assert_attributes(post_obj,attrs)

    
    async def test_animation(self):
        attrs = TESTDATA["animation"]["FractalGIF"]
        data,filepath = self.load_testdata(attrs)
        post_obj = await posts.create(data,filepath)
        
        self.assertEqual(post_obj.media_type,"animation")
        self.assertIsInstance(post_obj.full,schemas.Animation)
        self.assertIsInstance(post_obj.thumbnail,schemas.Image)
        self.assert_attributes(post_obj,attrs)

    
    async def test_video(self):
        attrs = TESTDATA["video"]["heavy"]
        data,filepath = self.load_testdata(attrs)
        post_obj = await posts.create(data,filepath)
        
        self.assertEqual(post_obj.media_type,"video")
        self.assertIsInstance(post_obj.full,schemas.Video)
        self.assertIsInstance(post_obj.thumbnail,schemas.Image)
        self.assert_attributes(post_obj,attrs)


