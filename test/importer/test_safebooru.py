from modules import database
from modules.importers import Safebooru
import pytest


@pytest.mark.asyncio
async def test_safebooru():
    database.Post.clear()
    importer = Safebooru()
    await importer.load(100)
    assert database.Post.count() == 100
