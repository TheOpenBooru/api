from modules import database
from modules.importers import E621
import pytest


@pytest.mark.asyncio
async def test_e621():
    database.Post.clear()
    importer = E621()
    await importer.load(100)
    assert database.Post.count() > 1
