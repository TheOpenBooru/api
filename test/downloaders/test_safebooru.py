from modules import downloaders
import pytest

"""
- Check that a user is exausted
- Can a tweet can be imported
"""

safebooru = downloaders.Safebooru()
SkipCondition = pytest.mark.skipif(safebooru.functional == False, reason="Safebooru Not Functional")


@SkipCondition
@pytest.mark.asyncio
async def test_Safebooru_Import_ID():
    url = "https://safebooru.org/index.php?page=post&s=view&id=1488313"
    posts = await safebooru.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "image"
    assert post.full.height == 513
    assert post.full.width == 452
