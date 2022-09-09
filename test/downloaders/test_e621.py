from modules import downloaders
import pytest

@pytest.fixture
def e621():
    return downloaders.E621()


@pytest.mark.asyncio
async def test_E621_is_valid_url(e621: downloaders.E621):
    assert e621.is_valid_url("https://e621.net/posts/2294957")
    assert e621.is_valid_url("https://e621.net/posts/2294957?q=test")
    assert not e621.is_valid_url("https://e621.net/posts/")


@pytest.mark.asyncio
async def test_Importing_Image(e621: downloaders.E621):
    url = "https://e621.net/posts/2294957"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "image"
    assert post.full.width == 1085
    assert post.full.height == 1132
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Image_With_Parameters(e621: downloaders.E621):
    url = "https://e621.net/posts/2294957?q=order%3Ascore+comic"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "image"
    assert post.full.width == 1085
    assert post.full.height == 1132
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Animation(e621: downloaders.E621):
    url = "https://e621.net/posts/1047489"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "animation"
    assert post.full.width == 70
    assert post.full.height == 124
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Video(e621: downloaders.E621):
    url = "https://e621.net/posts/2972352"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "video"
    assert post.full.width == 560
    assert post.full.height == 560
    assert len(post.tags) > 10
