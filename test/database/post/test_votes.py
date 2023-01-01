from . import ExamplePost
from openbooru.modules import schemas
from openbooru.modules.database import Post
from . import TestCase, generate_post


class test_Votes(TestCase):
    def setUp(self) -> None:
        self.post = generate_post()
        Post.insert(self.post)

    def test_Update_Doesnt_Affect_Object(self):
        post = self.post
        Post.add_upvote(post.id)
        assert Post.get_id(post.id).upvotes == 1
        Post.add_upvote(post.id)
        assert Post.get_id(post.id).upvotes == 2
