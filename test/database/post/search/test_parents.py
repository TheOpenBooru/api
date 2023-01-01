from . import ExamplePost, assertPostInSearch
from openbooru.modules import database, schemas
import pytest


def test_Tag_Parents_Search(ExamplePost: schemas.Post):
    database.clear()
    database.Tag.insert(schemas.Tag(name="mario", parents=["super_mario_bros"]))
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["super_mario_bros"]
    ))
    assertPostInSearch(post.id, search_response)


@pytest.mark.skip("TODO: Fix Chained Parents Search")
def test_Tag_Parents_Chained_Search(ExamplePost: schemas.Post):
    database.clear()
    database.Tag.insert(schemas.Tag(name="mario", parents=["super_mario_bros"]))
    database.Tag.insert(schemas.Tag(name="super_mario_bros", parents=["nintendo"]))
    
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["nintendo"]
    ))
    assertPostInSearch(post.id, search_response)
