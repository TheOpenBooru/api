from . import TestCase, generate_post
from modules.database import Post


class test_Update(TestCase):
    def setUp(self) -> None:
        self.post = generate_post()
        Post.create(self.post)
    
    def test_Update_Doesnt_Affect_Object(self):
        post = self.post
        new_post = post.copy()
        new_post.tags = ["safe"]
        Post.update(post.id,new_post)
        assert Post.get(id=post.id) == new_post
        assert Post.get(id=post.id) != post
