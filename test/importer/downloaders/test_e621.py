from modules import importers, schemas
import pytest


@pytest.fixture
def e621():
    return importers.E621Downloader()


@pytest.mark.asyncio
async def test_Nonexistant_Post_Raises_DownloadFailure(e621: importers.E621Downloader):
    with pytest.raises(importers.DownloadFailure):
        await e621.download_url("https://e621.net/posts/1")


@pytest.mark.asyncio
async def test_Importing_Image(e621: importers.E621Downloader):
    url = "https://e621.net/posts/2294957"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert url in post.sources
    assert post.full.type == schemas.MediaType.image
    assert post.full.width == 1085
    assert post.full.height == 1132
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Image_With_Parameters(e621: importers.E621Downloader):
    url = "https://e621.net/posts/2294957?q=order%3Ascore+comic"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert "https://e621.net/posts/2294957" in post.sources
    assert post.full.type == schemas.MediaType.image
    assert post.full.width == 1085
    assert post.full.height == 1132
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Animation(e621: importers.E621Downloader):
    url = "https://e621.net/posts/1047489"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert url in post.sources
    assert post.full.type == schemas.MediaType.animation
    assert post.full.width == 70
    assert post.full.height == 124
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Video(e621: importers.E621Downloader):
    url = "https://e621.net/posts/2972352"
    posts = await e621.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert url in post.sources
    assert post.full.type == schemas.MediaType.video
    assert post.full.width == 560
    assert post.full.height == 560
    assert len(post.tags) > 10
