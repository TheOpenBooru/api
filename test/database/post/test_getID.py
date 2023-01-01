from . import TestCase, generate_post
from openbooru.modules.database import Post
import unittest


class test_isnt_Used_By_Post(TestCase):
    def test_isnt_Used_By_Post(self):
        id = Post.generate_id()
        self.assertRaises(KeyError,Post.get,id)


class test_Is_Unique_When_Deleted_and_ReAdded(TestCase):
    def test_Is_Unique_When_Deleted_and_ReAdded(self):
        IDs = set()
        for _ in range(5):
            id = Post.generate_id()
            assert id not in IDs, f"ID {id} is not unique"
            
            IDs.add(id)
            post = generate_post(id)
            Post.insert(post)
            Post.delete(post.id)

