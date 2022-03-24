"""
Requirements:
get_unused_id:
    - IDs are unique
    - IDs are sequential
create:
    - Prevents Duplicates:
        - IDs
        - MD5s
        - SHA256s
    - Validates Data:
        - Uploader ID
        - Type
        - Rating
        - Language
update:
    - The post becomes the new version
search:
    - Orders Correctly
    - Appends at limit
    - Does not have max limit
delete:
    - Entries cannot be gotten
    - Allows deletion of non-existent entries
"""

from modules.database import Post
from modules import schemas
import unittest


def generate_post(id:int|None = None) -> schemas.Post:
    example_image = schemas.Image(
        url="https://example.com/image.png",
        height=100,width=100,
        mimetype='image/png'
    )
    if id is None:
        id = Post.get_unused_id()
    return schemas.Post(
        id=id,uploader=0,
        media_type="image",
        thumbnail=example_image,
        full=example_image,
    )

class test_Get_Unused_ID(unittest.TestCase):
    def tearDown(self):
        Post.clear()
    
    def test_isnt_Used_By_Post(self):
        id = Post.get_unused_id()
        assert Post.get(id=id) == None
    
    def test_is_Unique_when_deleted_and_Re_Added(self):
        IDs = set()
        for _ in range(1_000):
            id = Post.get_unused_id()
            assert id not in IDs, f"ID {id} is not unique"
            
            IDs.add(id)
            post = generate_post(id)
            Post.create(post)
            Post.delete(post.id)


    def test_is_Sequential_when_deleted(self):
        start_id = Post.get_unused_id()
        for x in range(5_000):
            id = Post.get_unused_id()
            assert id == start_id + x, f"ID {id} was not sequential"
            
            post = generate_post(id)
            Post.create(post)
            Post.delete(post.id)


class test_Create(unittest.TestCase):
    def test_a(self):
        post = generate_post()
        Post.create(post)
        assert post == Post.get(id=post.id)

class test_Edit(unittest.TestCase):
    def test_a(self):
        post = generate_post()
        Post.create(post)
        post.age_rating = "safe"
        Post.update(post.id,post)
        assert post == Post.get(id=post.id)

class test_Delete(unittest.TestCase):
    def test_allows_non_existant_ID(self):
        Post.delete(Post.get_unused_id())

    def test_deletes_removes_entries(self):
        post = generate_post()
        Post.create(post)
        Post.delete(post.id)
        assert Post.get(id=post.id) == None, "Post was not deleted"