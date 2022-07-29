from modules import importing, settings
import pytest

twitter = importing.Twitter()
SkipCondition = pytest.mark.skipif(twitter.functional == False, reason="Twitter Not Functional")
settings.TAGS_TAGGING_SERVICE_ENABLED = False


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Video_Tweet():
    tweet = "https://twitter.com/OpenBooru/status/1537464462063677441?s=20&t=oInfaI6U8aQCNJDivAK4mQ"
    posts = await twitter.import_url(tweet)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "video"
    assert post.source == tweet
    assert "openbooru" in post.tags

@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Image_Tweet():
    tweet = "https://twitter.com/AdvosArt/status/1551131534723547136"
    posts = await twitter.import_url(tweet)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "image"
    assert post.source == tweet
    assert "advosart" in post.tags

@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Text_Tweet():
    tweet = "https://twitter.com/OpenBooru/status/1552791748925161472?s=20"
    posts = await twitter.import_url(tweet)
    
    assert len(posts) == 0


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Tweet_Grabs_All_Image():
    tweet = "https://twitter.com/OpenBooru/status/1531028668667121665"
    posts = await twitter.import_url(tweet)
    assert len(posts) == 2
