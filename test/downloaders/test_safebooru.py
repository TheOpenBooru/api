from modules import downloaders
import pytest

@pytest.fixture
def safebooru():
    return downloaders.Safebooru()


@pytest.mark.asyncio
async def test_Safebooru_Import_ID(safebooru: downloaders.Safebooru):
    url = "https://safebooru.org/index.php?page=post&s=view&id=1488313"
    posts = await safebooru.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "image"
    assert post.full.height == 513
    assert post.full.width == 452
