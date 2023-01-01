from . import ExamplePost, assertPostInSearch
from openbooru.modules import database, schemas, posts


def test_Empty_Query_Returns_All_Posts(ExamplePost: schemas.Post):
    database.clear()
    post = ExamplePost
    database.Post.insert(post)
    search_response = database.Post.search(schemas.PostQuery())
    assertPostInSearch(post.id, search_response)


def test_Single_Tag_Search(ExamplePost: schemas.Post):
    database.clear()
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["mario"]
    ))
    
    assertPostInSearch(post.id, search_response)


def test_Multiple_Tags_Search(ExamplePost: schemas.Post):
    database.clear()
    post_1 = ExamplePost.copy()
    post_1.id = 1
    post_1.tags = ["mario","luigi"]
    database.Post.insert(post_1)
    
    post_2 = ExamplePost.copy()
    post_2.id = 2
    post_2.tags = ["mario"]
    database.Post.insert(post_2)

    query = schemas.PostQuery(include_tags=["mario","luigi"])
    search_response = database.Post.search(query)
    
    post_ids = [post.id for post in search_response]
    assert post_1.id in post_ids
    assert post_2.id not in post_ids
    

