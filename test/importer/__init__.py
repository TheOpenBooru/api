from modules import database
from unittest import IsolatedAsyncioTestCase as AsyncTestCase

class TestCase(AsyncTestCase):
    def asyncSetUp(self) -> None:
        database.Post.clear()
    
    def asyncTearDown(self) -> None:
        database.Post.clear()