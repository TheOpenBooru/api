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
        post = Post.md5_get(self.md5)
        assert post == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.md5_get,"f"*32)


class test_getBySHA256(TestCase):
    def setUp(self):
        self.post = generate_post()
        self.sha256 = bytes.fromhex("a"*64)
        self.post.hashes.sha256s = [self.sha256]
        Post.insert(self.post)

    def test_Retrieves_Successfully(self):
        assert Post.sha256_get(self.sha256) == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.sha256_get,"f"*64)
