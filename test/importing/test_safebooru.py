from modules import database, importing
import pytest

"""
- Check that a user is exausted
- Can a tweet can be imported
"""

safebooru = importing.Safebooru()
SkipCondition = pytest.mark.skipif(safebooru.functional == False, reason="Safebooru Not Functional")

@pytest.fixture
def ClearDatabase():
    database.clear()


@SkipCondition
@pytest.mark.asyncio
async def test_Safebooru_Import_ID(ClearDatabase):
    url = "https://safebooru.org/index.php?page=post&s=view&id=1488313"
    posts = await safebooru.import_url(url)
    assert len(posts) == 1
    post = posts[0]