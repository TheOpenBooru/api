from openbooru.modules.importers import Rule34Downloader
from openbooru.modules import schemas
import pytest


@pytest.fixture
def r34():
    return Rule34Downloader()


@pytest.mark.asyncio
async def test_Importing_Image(r34: Rule34Downloader):
    url = "https://rule34.xxx/index.php?page=post&s=view&id=5198120"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.full.type == schemas.MediaType.image
    assert post.full.width == 1534
    assert post.full.height == 1494
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Animation(r34: Rule34Downloader):
    url = "https://rule34.xxx/index.php?page=post&s=view&id=4138445"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.full.type == schemas.MediaType.animation
    assert post.full.width == 600
    assert post.full.height == 856
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Video(r34: Rule34Downloader):
    url = "https://rule34.xxx/index.php?page=post&s=view&id=3506721"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.full.type == schemas.MediaType.video
    assert post.full.width == 1280
    assert post.full.height == 720
    assert len(post.tags) > 10
