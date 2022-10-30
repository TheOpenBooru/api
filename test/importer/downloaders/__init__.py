from modules import database, settings
from unittest import IsolatedAsyncioTestCase as AsyncTestCase
settings.TAGS_TAGGING_SERVICE_ENABLED = False

class TestCase(AsyncTestCase):
    def asyncSetUp(self) -> None:
        database.Post.clear()
    
    def asyncTearDown(self) -> None:
        database.Post.clear()