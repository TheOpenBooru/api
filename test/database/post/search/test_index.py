from . import ExamplePost
from openbooru.modules import posts, schemas, database

def test_Index_Offsets_Post_Search(ExamplePost: schemas.Post):
    database.clear()
    post_1 = ExamplePost.copy()
    post_2 = ExamplePost.copy()
    post_1.id = 1
    post_2.id = 2
    database.Post.insert(post_1)
    database.Post.insert(post_2)
    
    index_0_posts = database.Post.search(schemas.PostQuery(limit=2))
    index_1_posts = database.Post.search(schemas.PostQuery(limit=2,index=1))
    assert index_0_posts[1:2] == index_1_posts[0:1]
    assert len(index_1_posts) == 1
