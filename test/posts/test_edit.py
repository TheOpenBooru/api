from modules import posts, schemas, database
from . import ExamplePost
import pytest


@pytest.mark.asyncio
async def test_Posts_Update_All_Correct(ExamplePost: schemas.Post):
    post = ExamplePost
    await posts.insert(post)
    posts.edit(
        post_id=post.id,
        editter_id=None,
        tags=post.tags,
        sources=post.sources,
        rating=schemas.Rating.explicit,
    )
    updated_post = database.Post.get(post.id)
    
    assert updated_post.tags == post.tags
    assert updated_post.sources == post.sources
    assert updated_post.rating == schemas.Rating.explicit
    assert len(updated_post.edits) == 1
    
    edit = updated_post.edits[0]
    assert edit.post_id == updated_post.id
    assert edit.editter_id == None
    assert edit.tags == updated_post.tags
    assert edit.sources == updated_post.sources
    assert edit.rating == schemas.Rating.explicit
