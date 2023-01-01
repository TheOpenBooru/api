from openbooru.modules import importers
from openbooru.modules.schemas import MediaType, Rating
from dataclasses import dataclass
import pytest


@dataclass(frozen=True)
class PostAssertion:
    type: MediaType
    height: int
    width: int


@dataclass(frozen=True, repr=True)
class DownloaderTestData:
    importer: importers.Downloader
    url: str
    assertions: list[PostAssertion]


file_importer = importers.FileDownloader()
data = (
    DownloaderTestData(
        importer=file_importer,
        url="https://cdn.discordapp.com/attachments/901797932595052566/1053040541446713394/F9E38D53-DA01-46AC-B068-1235CAE0261F.png",
        assertions=[
            PostAssertion(
                type=MediaType.image,
                height=611,
                width=567,
            )
        ]
    ),
)

@pytest.mark.parametrize("data", data)
@pytest.mark.asyncio
async def test_downloader_url(data: DownloaderTestData):
    importer = data.importer
    url = data.url
    assertions = data.assertions
    
    posts = await importer.download_url(url)

    for post, assertion in zip(posts, assertions):
        assert url in post.sources
        assert post.full.type == assertion.type
        assert post.full.width == assertion.height
        assert post.full.height == assertion.width

