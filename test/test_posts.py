from modules import posts,schemas,importer,settings
import yaml
from unittest import IsolatedAsyncioTestCase as AsyncTestCase


class test_Post_Create_has_Correct_Attributes(AsyncTestCase):
    async def asyncSetUp(self):
        with open('./data/test/sample_data.json','r') as f:
            self.testdata = yaml.full_load(f)
    
    def assert_attributes(self,post:schemas.Post,attrs:dict):
        assert post.full.width == attrs["width"],f'{post.full.width} != {attrs["width"]}'
        assert post.full.height == attrs["height"],f'{post.full.height} != {attrs["height"]}'
        if "duration" in attrs:
            self.assertAlmostEqual(post.full.duration,attrs["duration"],places=2)
        if "framerate" in attrs:
            self.assertEqual(post.full.fps,attrs["framerate"])
        if "hasAudio" in attrs:
            self.assertEqual(post.full.has_sound,attrs["hasAudio"])
            assert post.full.has_sound == attrs["hasAudio"],attrs["hasAudio"] # type:ignore

    def load_testdata(self,attrs:dict) -> tuple[bytes,str]:
        filepath = attrs['file']
        attrs.pop('file')
        with open(filepath,'rb') as f:
            data = f.read()
        return data,filepath

    async def test_image(self):
        attrs = self.testdata["image"]["Complex"]
        data,filepath = self.load_testdata(attrs)
        post_obj = await posts.create(data,filepath)
        
        self.assertEqual(post_obj.media_type,"image")
        self.assertIsInstance(post_obj.full,schemas.Image)
        self.assertIsInstance(post_obj.thumbnail,schemas.Image)
        self.assert_attributes(post_obj,attrs)
    
    async def test_animation(self):
        attrs = self.testdata["animation"]["FractalGIF"]
        data,filepath = self.load_testdata(attrs)
        post_obj = await posts.create(data,filepath)
        
        self.assertEqual(post_obj.media_type,"animation")
        self.assertIsInstance(post_obj.full,schemas.Animation)
        self.assertIsInstance(post_obj.thumbnail,schemas.Image)
        self.assert_attributes(post_obj,attrs)
    
    async def test_video(self):
        attrs = self.testdata["video"]["heavy"]
        data,filepath = self.load_testdata(attrs)
        post_obj = await posts.create(data,filepath)
        
        self.assertEqual(post_obj.media_type,"video")
        self.assertIsInstance(post_obj.full,schemas.Video)
        self.assertIsInstance(post_obj.thumbnail,schemas.Image)
        self.assert_attributes(post_obj,attrs)

class test_Post_Search(AsyncTestCase):
    async def asyncSetUp(self):
        await importer.import_safebooru(1000)
    
    async def test_limit_is_correct(self):
        query = schemas.Post_Query()
        searched_posts = await posts.search(query)
        assert len(searched_posts) == query.limit

    async def test_Post_Search_Returns_Posts(self):
        query = schemas.Post_Query()
        searched_posts = await posts.search(query)
        self.assertIsInstance(searched_posts,list)
        for post in searched_posts:
            assert isinstance(post,schemas.Post)

    async def test_Post_Search_Respects_Limit_in_Settings(self):
        query = schemas.Post_Query(limit=1_000_000)
        searched_posts = await posts.search(query)
        max_limit = settings.MAX_SEARCH_LIMIT
        assert len(searched_posts) <= max_limit

    
    async def test_Post_Search_Converts_Negative_Limit_To_Zero(self):
        query = schemas.Post_Query(limit=-2)
        searched_posts = await posts.search(query)
        assert len(searched_posts) == 0
