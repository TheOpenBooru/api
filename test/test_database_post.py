from modules.database import Post
from modules import schemas
import unittest
from typing import Union


def generate_post(id:Union[int,None] = None) -> schemas.Post:
    EXAMPLE_IMAGE = schemas.Image(
        url="https://example.com/image.png",
        height=100,width=100,
        mimetype='image/png'
    )
    id = id or Post.get_unused_id()
    return schemas.Post(
        id=id,uploader=0,
        media_type="image",
        thumbnail=EXAMPLE_IMAGE,
        full=EXAMPLE_IMAGE,
    )

class TestCase(unittest.TestCase):
    def setUp(self):
        Post.clear()
    def tearDown(self):
        Post.clear()



class test_Post_Count(TestCase):
    def test_Count_Is_Updated_Correctly(self):
        Post.create(generate_post(1))
        assert Post.count() == 1
        Post.create(generate_post(2))
        assert Post.count() == 2


class test_Get_Unused_ID(TestCase):
    def test_isnt_Used_By_Post(self):
        id = Post.get_unused_id()
        self.assertRaises(KeyError,Post.get,id)
    
    def test_is_Unique_when_deleted_and_Re_Added(self):
        IDs = set()
        for _ in range(10):
            id = Post.get_unused_id()
            assert id not in IDs, f"ID {id} is not unique"
            
            IDs.add(id)
            post = generate_post(id)
            Post.create(post)
            Post.delete(post.id)


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
        post_b.md5s = post_a.md5s = ['f'*32]
        Post.create(post_a)
        self.assertRaises(KeyError,Post.create,post_b)
    
    def test_prevents_duplicates_sha256(self):
        post_a = generate_post()
        post_a.sha256s = ['f'*64]
        Post.create(post_a)
        post_b = generate_post()
        post_b.sha256s = ['f'*64]
        self.assertRaises(KeyError,Post.create,post_b)


class test_Update(TestCase):
    def setUp(self) -> None:
        self.post = generate_post()
        Post.create(self.post)
    
    def test_a(self):
        post = self.post
        new_post = post.copy()
        new_post.tags = ["safe"]
        Post.update(post.id,new_post)
        assert Post.get(id=post.id) == new_post
        assert Post.get(id=post.id) != post


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


class test_Clear(TestCase):
    def test_Clear_Removes_All_Posts(self):
        Post.create(generate_post())
        Post.clear()
        assert Post.count() == 0


class test_Increment_View(TestCase):
    def setUp(self):
        self.post = post = generate_post()
        Post.create(post)
    
    def test_Increment_View(self):
        id = self.post.id
        for x in range(1,10):
            Post.increment_view(id)
            post = Post.get(id)
            assert post
            assert post.views == x, "Could not increment views"

class test_DatabasePosts_getByMD5(TestCase):
    def setUp(self):
        self.post = generate_post()
        self.md5 = "a"*32
        self.post.md5s = [self.md5]
        Post.create(self.post)

    def test_Retrieves_Successfully(self):
        assert Post.getByMD5(self.md5) == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.getByMD5,"f"*16)

class test_DatabasePosts_getBySHA256(TestCase):
    def setUp(self):
        self.post = generate_post()
        self.sha256 = "a"*64
        self.post.sha256s = [self.sha256]
        Post.create(self.post)

    def test_Retrieves_Successfully(self):
        assert Post.getBySHA256(self.sha256) == self.post
    
    def test_NonExistant_Raises_Error(self):
        self.assertRaises(KeyError,Post.getBySHA256,"f"*32)