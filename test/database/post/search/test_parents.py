from . import ClearDatabase, ExamplePost
from modules import database, schemas, posts


def test_Tag_Parents_Search(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(name="mario", parents=["super_mario_bros"]))
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["super_mario_bros"]
    ))


def test_Tag_Parents_Chained_Search(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(name="mario", parents=["super_mario_bros"]))
    database.Tag.insert(schemas.Tag(name="super_mario_bros", parents=["nintendo"]))
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)
    
    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["nintendo"]
    ))
