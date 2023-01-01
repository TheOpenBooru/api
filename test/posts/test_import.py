from . import ExamplePost
from openbooru.modules import posts, schemas, importers, settings, database
import pytest


@pytest.mark.asyncio
async def test_Posts_Imports_Inserts_Posts(ExamplePost):
    database.clear()
    url = "https://twitter.com/OpenBooru/status/1541087046856474624/photo/3"
    await posts.Import(url, user_id=1)
    _posts = await posts.search()
    for post in _posts:
        assert post.uploader == 1
        assert "https://twitter.com/OpenBooru/status/1541087046856474624/photo/3" in post.sources



@pytest.mark.asyncio
async def test_Double_Insertion_Raises_Error(ExamplePost):
    database.clear()
    await posts.insert(ExamplePost)
    with pytest.raises(posts.PostExistsException):
        await posts.insert(ExamplePost)
