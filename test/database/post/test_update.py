from . import TestCase, create_post
from modules import schemas
from modules.database import Post
import pytest


def test_Update_Modifies_Post():
    post = create_post()
    edit = schemas.PostEdit(
        post_id=post.id,
        tags=["safe"],
        sources=["https://twitter.com"],
        rating=schemas.Rating.safe
    )
    
    Post.edit(post.id, edit)
    updated_post = Post.get(post.id)
    assert edit in updated_post.edits
    assert updated_post.tags == ["safe"]
    assert updated_post.sources == ["https://twitter.com"]
    assert updated_post.rating == schemas.Rating.safe


def test_Update_Doesnt_Mutate_Input():
    post = create_post()
    edit = schemas.PostEdit(
        post_id=post.id,
        tags=["safe"],
        sources=["https://twitter.com"],
        rating=schemas.Rating.safe
    )

    old_post = post.copy()
    Post.edit(post.id, edit)
    assert old_post == post
