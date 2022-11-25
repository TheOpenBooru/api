from . import ExamplePost
from modules import posts, schemas, importers, settings, database
import pytest


async def test_Posts_Insert_Actually_Inserts(ExamplePost):
    database.clear()
    await posts.insert(ExamplePost)
    _posts = await posts.search()
    assert ExamplePost in _posts



async def test_Double_Insertion_Raises_Error(ExamplePost):
    database.clear()
    await posts.insert(ExamplePost)
    with pytest.raises(posts.PostExistsException):
        await posts.insert(ExamplePost)
