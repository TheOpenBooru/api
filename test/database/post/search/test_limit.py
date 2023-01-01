from . import generate_post
from openbooru.modules import database, schemas
import pytest


def test_Searches_Are_Limited_By_Query():
    database.clear()
    for _ in range(5):
        post = generate_post()
        database.Post.insert(post)
    
    search_response = database.Post.search(schemas.PostQuery(
        limit=2
    ))
    assert len(search_response) == 2
