from . import ExamplePost, ClearDatabase
from modules import posts, schemas, importers, settings, database
import pytest

@pytest.mark.asyncio
async def test_Posts_Insert_Actually_Inserts(ClearDatabase, ExamplePost):
    await posts.insert(ExamplePost)
    _posts = await posts.search()
    assert ExamplePost in _posts


@pytest.mark.asyncio
async def test_Double_Insertion_Raises_Error(ClearDatabase, ExamplePost):
    await posts.insert(ExamplePost)
    with pytest.raises(posts.PostExistsException):
        await posts.insert(ExamplePost)
