import os
import unittest
from modules import database
from modules.database import Image, Post, User

os.environ["DEPLOYMENT"] = "TESTING"

imageData = {
    "url": "https://example.com/image.jpeg",
    "md5": "ffffffffffffffffffffffffffffffff",
    "height": 500,
    "width": 500,
    "mimetype": "image/jpeg",
}
userData = {"name": "example_user", "email": "test@example.com"}


class test_Create_Account(unittest.TestCase):
    def setUp(self):
        database.clear()

    def tearDown(self) -> None:
        database.clear()

    def test_Create_User(self):
        userID = User.create("example_user", "test@example.com")
        self.assertIsInstance(userID,int,"Didn't return interger ID")
        user = User.get(id=userID)
        self.assertEquals(user["name"], "example_user")
        self.assertEquals(user["private"]["email"], "test@example.com")


class test_Create_Image(unittest.TestCase):
    def setUp(self):
        database.clear()

    def tearDown(self) -> None:
        database.clear()

    def test_Create_Image(self):
        imgID = Image.create(**imageData)
        self.assertIsInstance(imgID,int,"Didn't return interger ID")
        img = Image.get(md5=imageData["md5"])
        self.assertDictContainsSubset(
            imageData, img, "Data was not stored correctly by "
        )


class test_Create_Post(unittest.TestCase):
    def setUp(self):
        database.clear()
        self.imgID = Image.create(**imageData)
        self.userID = User.create(**userData)

    def tearDown(self) -> None:
        database.clear()

    def test_Create_Post(self):
        postData = {
            "creator_id": self.userID,
            "full_id": self.imgID,
            "preview_id": self.imgID,
            "thumbnail_id": self.imgID,
            "type": "image",
            "sound": False,
            "source": "https://example.com/image.jpeg",
            "rating": "safe",
        }
        postID = Post.create(**postData)
        self.assertIsInstance(postID,int,"Didn't return interger ID")
        post = Post.get(id=postID)
        self.assertDictContainsSubset(postData, post)