"""Requirements:
- Valid Request should return
- Valid ID should return 200 Status Code
- Non-existant ID should return 404 Status Code
"""
import requests
import unittest
from modules.schemas import Post

class test_get(unittest.TestCase):
    def test_Nonexistant_ID_Should_Return_404(self):
        r = requests.get("http://slate:57255/posts/post?id=-1")
        self.assertEqual(r.status_code, 404)
    def test_Valid_ID_Should_Return_202(self):
        r = requests.get("http://slate:57255/posts/post?id=1")
        self.assertEqual(r.status_code, 200)
        post = Post.construct(**r.json())
        self.assertEqual(post.id, 1)
