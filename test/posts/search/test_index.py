from . import ClearDatabase, ExamplePost
from modules import posts, schemas, database
import pytest


def test_Index_Offsets_Post_Search(ClearDatabase, ExamplePost: schemas.Post):
    
    index_0_posts = database.Post.search(schemas.PostQuery(limit=2))
    index_1_posts = database.Post.search(schemas.PostQuery(limit=2,index=0))
    assert index_0_posts[1:2] == index_1_posts[0:1]
    assert len(index_1_posts) == 1
