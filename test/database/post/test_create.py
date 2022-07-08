from . import TestCase, generate_post
from modules.database import Post

class test_Create(TestCase):
    def test_Created_Posts_can_be_retrieved(self):
        post = generate_post()
        Post.create(post)
        assert post == Post.get(post.id)

        
    def test_prevents_duplicates_ids(self):
        post_a = generate_post()
        post_b = generate_post()
        post_b.id = post_a.id
        Post.create(post_a)
        self.assertRaises(KeyError,Post.create,post_b)

    
    def test_prevents_duplicates_md5s(self):
        post_a = generate_post()
        post_b = generate_post()
        post_b.hashes.md5s = post_a.hashes.md5s = ['f'*32]
        Post.create(post_a)
        self.assertRaises(KeyError,Post.create,post_b)

    
    def test_prevents_duplicates_sha256(self):
        post_a = generate_post()
        post_a.hashes.sha256s = ['f'*64]
        Post.create(post_a)
        post_b = generate_post()
        post_b.hashes.sha256s = ['f'*64]
        self.assertRaises(KeyError,Post.create,post_b)
