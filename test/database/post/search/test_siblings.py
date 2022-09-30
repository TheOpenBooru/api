from . import ClearDatabase, ExamplePost, assertPostInSearch
from modules import database, schemas, settings

settings.POSTS_SEARCH_USE_SIBLINGS_AND_PARENTS = True


def test_Tag_Siblings_Search(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(
        name="mario", siblings=["mario_(super_mario_bros)"]
    ))
    
    post = ExamplePost.copy()
    post.tags = ["mario"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["mario_(super_mario_bros)"]
    ))
    
    assertPostInSearch(post.id, search_response)


def test_Tag_Siblings_Backwards(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(
        name="mario", siblings=["mario_(super_mario_bros)"]
    ))
    
    post = ExamplePost.copy()
    post.tags = ["mario_(super_mario_bros)"]
    database.Post.insert(post)

    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["mario"]
    ))
    assertPostInSearch(post.id, search_response)

 
def test_Tag_Chained_Siblings_Search(ClearDatabase, ExamplePost: schemas.Post):
    database.Tag.insert(schemas.Tag(
        name="zelda",
        siblings=["princess_zelda", "zelda_(legend_of_zelda)"]
    ))
    
    post = ExamplePost.copy()
    post.tags = ["princess_zelda"]
    database.Post.insert(post)
    
    search_response = database.Post.search(schemas.PostQuery(
        include_tags=["zelda_(legend_of_zelda)"]
    ))
    assertPostInSearch(post.id, search_response)
