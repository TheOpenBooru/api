from . import TestCase, generate_post
from modules.database import Post


class test_Count_Increments_With_Creation(TestCase):
    def test_Count_Increments_With_Creation(self):
        Post.insert(generate_post())
        assert Post.count() == 1
        Post.insert(generate_post())
        assert Post.count() == 2


class test_Count_Decrements_With_Deletions(TestCase):
    def test_Count_Decrements_With_Deletions(self):
        post = generate_post()
        Post.insert(post)
        assert Post.count() == 1
        Post.delete(post.id)
        assert Post.count() == 0
