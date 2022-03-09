from modules.search import SearchParameters,searchPosts
from modules import settings,schemas
from scripts import example_data


example_data.generate(100)

def test_Post_Searching_For_No_Tags_Returns_All_posts():
    params = SearchParameters()
    posts = searchPosts(params)
    assert len(posts) == params.limit


def test_Post_Search_Returns_Posts():
    params = SearchParameters()
    posts = searchPosts(params)
    assert isinstance(posts,list)
    for post in posts:
        assert isinstance(post,schemas.Post)


def test_Post_Search_Respects_Limit_in_Settings():
    params = SearchParameters(limit=1_000_000)
    max_limit = settings.get('settings.search.max_limit')
    posts = searchPosts(params)
    assert len(posts) == max_limit


def test_Post_Search_Converts_Negative_Limit_To_Zero():
    params = SearchParameters(limit=-2)
    posts = searchPosts(params)
    assert len(posts) == 0
