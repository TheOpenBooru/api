from .. import client
from ... import ExamplePost
from modules import posts, schemas
import pytest


@pytest.mark.asyncio
async def test_post_200(ExamplePost):
    await posts.insert(ExamplePost, validate=False)
    post_id = ExamplePost.id
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200
    response_post = schemas.Post.parse_obj(response.json())
    assert ExamplePost == response_post


def test_post_404():
    response = client.get("/post/404")
    assert response.status_code == 404
