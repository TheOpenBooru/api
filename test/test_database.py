import os
import unittest
from modules import database
from modules.database import Image, Post, Tag, User

os.putenv('DEPLOYMENT', 'TESTING')

class test_tag(unittest.TestCase):
    ...
    def test_a(self):
        Tag.create('test_a','generic')

class test_scenario_1(unittest.TestCase):
    def setUp(self):
        database.utils.clear()
    def tearDown(self):
        database.utils.clear()
    def test_a(self):
        UserID = User.create('test_a','user@example.com')
        ImageID = Image.create(
            "https://i.imgur.com/a83JD94.jpeg",
            550,1542,"image/jpeg")
        PostID = Post.create(
            UserID,
            ImageID,ImageID,ImageID,
            'f'*32,'f'*64,
            'en','exmaple.com','safe',
            'image',False
            )
        Post.get(PostID)
