from . import ClearDatabase, ExamplePost
from modules import database, schemas


def test_Tag_Siblings_Search(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(
        name="mario", siblings=["mario_(super_mario_bros)"]
    ))
    
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["mario_(super_mario_bros)"]
    ))


def test_Tag_Siblings_Backwards(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(
        name="mario", siblings=["mario_(super_mario_bros)"]
    ))
    
    post = ExamplePost.copy()
    post.tags = ["mario_(super_mario_bros)"]
    database.Post.insert(post)

    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["mario"]
    ))

 
def test_Tag_Chained_Siblings_Search(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(
        name="zelda",
        siblings=["princess_zelda", "zelda_(legend_of_zelda)"]
    ))
    
    post = ExamplePost.copy()
    post.tags = ["princess_zelda"]
    database.Post.insert(post)
    assert post == database.Post.search(schemas.PostQuery(
        include_tags=["zelda_(legend_of_zelda)"]
    ))