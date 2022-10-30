from modules import posts, schemas, importers, settings, database
import unittest

class test_Posts_Search(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        database.Post.clear()
        importer = importers.SafebooruImporter()
        await importer.load(limit=100)
        assert database.Post.count() == 100
        
        settings.POSTS_SEARCH_MAX_LIMIT = 20
    
    async def asyncTearDown(self):
        database.Post.clear()


    async def test_Returns_Posts(self):
        query = schemas.PostQuery(limit=10)
        searched_posts = await posts.search(query)
        assert len(searched_posts) > 0


    async def test_Posts_Are_Capped_To_Limit(self):
        query = schemas.PostQuery(limit=10)
        searched_posts = await posts.search(query)
        assert len(searched_posts) == query.limit


    async def test_Post_Search_Returns_Posts(self):
        query = schemas.PostQuery()
        searched_posts = await posts.search(query)
        self.assertIsInstance(searched_posts,list)
        for post in searched_posts:
            assert isinstance(post,schemas.Post)


    async def test_Post_Search_Respects_Limit_in_Settings(self):
        query = schemas.PostQuery(limit=1_000_000)
        searched_posts = await posts.search(query)
        max_limit = settings.POSTS_SEARCH_MAX_LIMIT
        assert len(searched_posts) == max_limit
