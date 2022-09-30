from . import ExamplePost, ClearDatabase
from modules import posts, schemas, importers, settings, database
import pytest

@pytest.mark.asyncio
async def test_Posts_Imports_Inserts_Posts(ClearDatabase, ExamplePost):
    url = "https://twitter.com/OpenBooru/status/1541087046856474624/photo/3"
    await posts.Import(url, user_id=1)
    _posts = await posts.search()
    for post in _posts:
        assert post.uploader == 1
        assert post.source.startswith("https://twitter.com/OpenBooru/status/1541087046856474624")


@pytest.mark.asyncio
async def test_Double_Insertion_Raises_Error(ClearDatabase, ExamplePost):
    await posts.insert(ExamplePost)
    with pytest.raises(posts.PostExistsException):
        await posts.insert(ExamplePost)
