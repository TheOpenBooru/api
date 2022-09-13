from . import TestCase, generate_post
from modules.database import Post


class test_get(TestCase):
    def setUp(self):
        self.post = generate_post()
        Post.insert(self.post)

    def test_Retrieves_Successfully(self):
        assert Post.get(self.post.id) == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.get,9999999999)


class test_getByMD5(TestCase):
    def setUp(self):
        self.post = generate_post()
        self.md5 = bytes.fromhex("a"*32)
        self.post.hashes.md5s = [self.md5]
        Post.insert(self.post)

    def test_Retrieves_Successfully(self):
        assert Post.getByMD5(self.md5) == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.getByMD5,"f"*32)


class test_getBySHA256(TestCase):
    def setUp(self):
        self.post = generate_post()
        self.sha256 = bytes.fromhex("a"*64)
        self.post.hashes.sha256s = [self.sha256]
        Post.insert(self.post)

    def test_Retrieves_Successfully(self):
        assert Post.getBySHA256(self.sha256) == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.getBySHA256,"f"*64)