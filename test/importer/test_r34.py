from modules import database
from modules.importers import Rule34
import pytest


@pytest.mark.asyncio
async def test_r34():
    database.Post.clear()
    importer = Rule34()
    await importer.load(100)
    assert database.Post.count() > 1
