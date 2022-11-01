from modules.importers import Rule34Downloader
import pytest


@pytest.fixture
def r34():
    return Rule34Downloader()


async def test_Rule34_Check_URL(r34: Rule34Downloader):
    assert r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=view&id=5198120")
    assert r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=view&id=5198120&test=1")
    assert not r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=view")
    assert not r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=list")
    assert not r34.is_valid_url("https://rule34.xxx/index.php?page=pool&s=show&id=21185")


async def test_Importing_Image(r34: Rule34Downloader):
    url = "https://rule34.xxx/index.php?page=post&s=view&id=5198120"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "image"
    assert post.full.width == 1534
    assert post.full.height == 1494
    assert len(post.tags) > 10


async def test_Importing_Animation(r34: Rule34Downloader):
    url = "https://rule34.xxx/index.php?page=post&s=view&id=4138445"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "animation"
    assert post.full.width == 600
    assert post.full.height == 856
    assert len(post.tags) > 10


async def test_Importing_Video(r34: Rule34Downloader):
    url = "https://rule34.xxx/index.php?page=post&s=view&id=3506721"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "video"
    assert post.full.width == 1280
    assert post.full.height == 720
    assert len(post.tags) > 10
