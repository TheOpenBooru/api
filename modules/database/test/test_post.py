from . import DATA,LOOKUP,clear
from . import Image,User,Post
import unittest

class test_Create_Post(unittest.TestCase):
    def setUp(self):
        clear()
        self.imgID = Image.create(**DATA.IMAGE)
        self.userID = User.create(**DATA.USER)

    def tearDown(self) -> None:
        Image.delete(self.imgID)
        User.delete(self.imgID)

    def test_Create_Post(self):
        postData = {
            "creator_id": self.userID,
            "full_id": self.imgID,
            "preview_id": self.imgID,
            "thumbnail_id": self.imgID,
        } | DATA.POST
        print(postData)
        postID = Post.create(**postData)
        self.assertIsInstance(postID,int,"Didn't return interger ID")
        post = Post.get(id=postID)
        self.assertDictContainsSubset(postData, post)

        for key,value in post.items():
            self.assertIn(key,LOOKUP.POST,f"Invalid Key '{key}' inside User")
            self.assertIsInstance(value,LOOKUP.POST[key])
