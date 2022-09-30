from . import ClearDatabase, ExamplePost, assertPostInSearch
from modules import database, schemas, posts


def test_Empty_Query_Returns_All_Posts(ClearDatabase, ExamplePost: schemas.Post):
    post = ExamplePost
    database.Post.insert(post)
    search_response = database.Post.search(schemas.PostQuery())
    assertPostInSearch(post.id, search_response)


def test_Single_Tag_Search(ClearDatabase, ExamplePost: schemas.Post):
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["mario","luigi"]
    ))
    
    assertPostInSearch(post.id, search_response)


def test_Multiple_Tags_Search(ClearDatabase, ExamplePost: schemas.Post):
    post = ExamplePost.copy()
    post.tags = ["mario","luigi"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["mario","luigi"]
    ))
    
    assertPostInSearch(post.id, search_response)

