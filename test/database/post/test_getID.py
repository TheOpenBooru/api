from . import TestCase, generate_post
from modules.database import Post


class test_isnt_Used_By_Post(TestCase):
    def test_isnt_Used_By_Post(self):
        id = Post.get_unused_id()
        self.assertRaises(KeyError,Post.get,id)


class test_Is_Unique_When_Deleted_and_ReAdded(TestCase):
    def test_Is_Unique_When_Deleted_and_ReAdded(self):
        IDs = set()
        for _ in range(5):
            id = Post.get_unused_id()
            assert id not in IDs, f"ID {id} is not unique"
            
            IDs.add(id)
            post = generate_post(id)
            Post.create(post)
            Post.delete(post.id)


class test_IDs_are_sequential(TestCase):
    def test_IDs_are_sequential(self):
        last_id = 0
        for _ in range(10):
            id = Post.get_unused_id()
            post = generate_post(id)
            Post.create(post)
            assert post.id == last_id + 1
            last_id = post.id