from . import TestCase, generate_post
from openbooru.modules.database import Post


class test_Clear(TestCase):
    def test_Clear_Removes_All_Posts(self):
        Post.insert(generate_post())
        assert Post.count() == 1
        Post.clear()
        assert Post.count() == 0
