# from modules.search import SearchParameters,searchPosts
# from modules import settings,schemas
# from scripts import example_data
# import unittest


# example_data.generate(100)
# class test_Post_Searching_For_No_Tags_Returns_All_posts(unittest.TestCase):
#     def test_a(self):
#         params = SearchParameters()
#         posts = searchPosts(params)
#         assert len(posts) == params.limit


# class test_Post_Search_Returns_Posts(unittest.TestCase):
#     def test_a(self):
#         params = SearchParameters()
#         posts = searchPosts(params)
#         self.assertIsInstance(posts,list)
#         for post in posts:
#             assert isinstance(post,schemas.Post)


# class test_Post_Search_Respects_Limit_in_Settings(unittest.TestCase):
#     def test_a(self):
#         params = SearchParameters(limit=1_000_000)
#         max_limit = settings.get('settings.search.max_limit')
#         posts = searchPosts(params)
#         assert len(posts) == max_limit


# class test_Post_Search_Converts_Negative_Limit_To_Zero(unittest.TestCase):
#     def test_a(self):
#         params = SearchParameters(limit=-2)
#         posts = searchPosts(params)
#         assert len(posts) == 0
