import unittest
from typing import Optional
from modules import schemas
from modules.database import Post


class TestCase(unittest.TestCase):
    def setUp(self):
        Post.clear()
    def tearDown(self):
        Post.clear()


def generate_post(id:Optional[int] = None) -> schemas.Post:
    EXAMPLE_IMAGE = schemas.Image(
        url="https://example.com/image.png",
        height=100,width=100,
        mimetype='image/png'
    )
    id = id or Post.generate_id()
    return schemas.Post(
        id=id,uploader=0,
        media_type="image",
        thumbnail=EXAMPLE_IMAGE,
        full=EXAMPLE_IMAGE,
    )
