from . import ExamplePost
from modules import database, schemas


def test_Upvotes(ExamplePost: schemas.Post):
    database.clear()
    database.Post.add_upvote(ExamplePost.id)
    assert database.Post.get_id(ExamplePost.id).upvotes == 1
    database.Post.add_upvote(ExamplePost.id)
    assert database.Post.get_id(ExamplePost.id).upvotes == 2
