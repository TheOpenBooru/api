from modules import importers
import pytest


@pytest.fixture
def twitter():
    return importers.TwitterDownloader()


@pytest.mark.asyncio
async def test_Invalid_URLs_Raise_DownloadFailure(twitter: importers.TwitterDownloader):
    bad_tweets = [
        "https://twitter.com/OpenBooru/1537464462063677441"
        "https://twitter.com/status/1537464462063677441"
        "https://twitter.com/"
    ]
    for url in bad_tweets:
        with pytest.raises(importers.DownloadFailure):
            await twitter.download_url(url)


@pytest.mark.asyncio
async def test_Importing_Video_Tweet(twitter: importers.TwitterDownloader):
    tweet = "https://twitter.com/OpenBooru/status/1537464462063677441?s=20&t=oInfaI6U8aQCNJDivAK4mQ"
    posts = await twitter.download_url(tweet)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "video"
    assert post.source == tweet
    assert "openbooru" in post.tags


@pytest.mark.asyncio
async def test_Importing_Animation_Tweet(twitter: importers.TwitterDownloader):
    tweet = "https://twitter.com/LykeIsland/status/1568355135012626435"
    posts = await twitter.download_url(tweet)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "video"
    assert post.source == tweet
    assert "lykeisland" in post.tags


@pytest.mark.asyncio
async def test_Importing_Image_Tweet(twitter: importers.TwitterDownloader):
    tweet = "https://twitter.com/AdvosArt/status/1551131534723547136"
    posts = await twitter.download_url(tweet)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "image"
    assert post.source == tweet
    assert "advosart" in post.tags


@pytest.mark.asyncio
async def test_Importing_Individual_Image(twitter: importers.TwitterDownloader):
    tweet = "https://twitter.com/OpenBooru/status/1566759990681026562/photo/2"
    posts = await twitter.download_url(tweet)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "image"
    assert post.source == tweet
    assert int(post.full.width / post.full.height) == 2
    assert "openbooru" in post.tags


@pytest.mark.asyncio
async def test_Importing_Text_Tweet(twitter: importers.TwitterDownloader):
    tweet = "https://twitter.com/OpenBooru/status/1552791748925161472"
    with pytest.raises(importers.DownloadFailure):
        await twitter.download_url(tweet)


@pytest.mark.asyncio
async def test_Importing_Tweet_Grabs_All_Image(twitter: importers.TwitterDownloader):
    tweet = "https://twitter.com/OpenBooru/status/1531028668667121665"
    posts = await twitter.download_url(tweet)
    assert len(posts) == 2
