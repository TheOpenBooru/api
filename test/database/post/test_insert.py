from . import TestCase, generate_post
from modules.database import Post

class test_Create(TestCase):
    def test_Created_Posts_can_be_retrieved(self):
        post = generate_post()
        Post.insert(post)
        assert post == Post.get(post.id)


    def test_prevents_duplicates_ids(self):
        post_a = generate_post()
        post_b = generate_post()
        post_b.id = post_a.id
        Post.insert(post_a)
        self.assertRaises(KeyError,Post.insert,post_b)
