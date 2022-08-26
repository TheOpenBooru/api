from modules import downloaders
import pytest

importer = downloaders.File()


@pytest.mark.asyncio
async def test_Valid_File_Url_Checks():
    invalid = [
        ("http://example.com/test.png","Non-https"),
        ("https:example.com/test.png","Bad "),
        ("https:example.com/test.png","Bad "),
    ]
    importer.is_valid_url()
    ...


@pytest.mark.asyncio
async def test_File_url_Importing_PNG():
    ...

@pytest.mark.asyncio
async def test_File_url_Importing_JPEG():
    url = "https://i.imgur.com/XMNnx42.jpeg"
    posts = await importer.download_url(url)


@pytest.mark.asyncio
async def test_File_url_Importing_WEBP():
    ...


@pytest.mark.asyncio
async def test_File_url_Importing_WEBM():
    ...


@pytest.mark.asyncio
async def test_File_url_Importing_MP4():
    ...
