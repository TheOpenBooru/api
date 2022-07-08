from . import TestCase, generate_post
from modules.database import Post

class test_Delete(TestCase):
    def setUp(self):
        super().setUp()
        self.post = post = generate_post()
        Post.create(post)
    
    def test_Allows_Deletion_of_NonExistant_Post(self):
        Post.delete(Post.get_unused_id())
    
    def test_Deletes_Successfully_Removes_Entries(self):
        self.post = post = generate_post()
        Post.create(post)
        post = self.post
        Post.delete(post.id)
        self.assertRaises(KeyError,Post.get,post.id)

