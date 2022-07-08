from modules import posts, schemas, importing, settings, database
import unittest

settings.STORAGE_METHOD = 'local'

importer = importing.Safebooru()

@unittest.skipUnless(importer.functional, "Could not import example data from SafeBooru")
class test_Post_Search(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await importer.import_default()
        settings.POSTS_SEARCH_MAX_LIMIT = 20
    
    async def asyncTearDown(self):
        database.Post.clear()
    
    
    async def test_Returns_Posts(self):
        query = schemas.Post_Query(limit=10)
        searched_posts = await posts.search(query)
        assert len(searched_posts) > 0
    
    async def test_Posts_Are_Capped_To_Limit(self):
        query = schemas.Post_Query(limit=10)
        searched_posts = await posts.search(query)
        assert len(searched_posts) == query.limit
    
    async def test_Index_Offsets_Post_Search(self):
        query = schemas.Post_Query(limit=10)
        index_0_posts = await posts.search(query)
        query.index = 1
        index_1_posts = await posts.search(query)
        assert index_0_posts[1:10] == index_1_posts[:9]
        assert len(index_1_posts) == query.limit

    async def test_Post_Search_Returns_Posts(self):
        query = schemas.Post_Query()
        searched_posts = await posts.search(query)
        self.assertIsInstance(searched_posts,list)
        for post in searched_posts:
            assert isinstance(post,schemas.Post)

    async def test_Post_Search_Respects_Limit_in_Settings(self):
        query = schemas.Post_Query(limit=1_000_000)
        searched_posts = await posts.search(query)
        max_limit = settings.POSTS_SEARCH_MAX_LIMIT
        assert len(searched_posts) == max_limit

    
    async def test_Post_Search_Converts_Negative_Limit_To_Zero(self):
        query = schemas.Post_Query(limit=-2)
        searched_posts = await posts.search(query)
        assert len(searched_posts) == settings.POSTS_SEARCH_MAX_LIMIT
